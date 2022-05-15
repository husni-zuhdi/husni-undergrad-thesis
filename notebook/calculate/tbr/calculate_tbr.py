import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import openmc
import paramak
import paramak_neutronics as nparamak
import neutronics_material_maker as nmm

def create_materials(enrich_Li, neutron_multi):
    """Set the materials required to run TBR calculation
    
    Parameters:
    -----------
    enrichment_Li : int, required
        Value of Li-6 enrichment in the Breeder Blanket.
        Example
            enrichment_Li=10 mean 10% enrichment of Li-6
    neutron_multi : float, optional
        Percentage of neutron multiplier (Natural Pb) in Moderator.
        Calculated by volume.
        Default = 0 (%).
        Example
            neutron_multi=0.5 mean 50% of moderator volume is Natural Pb.
    """
    # Plasma Material
    plasma_mat = nmm.Material(
        name='U235',
        isotopes={'U235':1},
        density=1e-6,
        percent_type='ao',
        density_unit='g/cm3'
    )
    plasma_mat.name = 'plasma_mat'
    plasma_mat.openmc_material
    
    # Plasma Facing Material
    blanket_pfc_mat = nmm.Material.from_library('Beryllium')
    blanket_pfc_mat.name = 'blanket_pfc_mat'
    blanket_pfc_mat.openmc_material
    
    # Cooper Alloy Heat Sink
    blanket_heat_sink_mat = nmm.Material.from_library('CuCrZr')
    blanket_heat_sink_mat.name = 'blanket_heat_sink_mat'
    blanket_heat_sink_mat.openmc_material
    
    # Blanket Fluid Material
    blanket_fluid_mat = nmm.Material.from_library(name='Lithium Fluoride',
                                            enrichment=enrich_Li,
                                            enrichment_target='Li6',
                                            enrichment_type='ao',
                                            temperature=1200,
                                            temperature_to_neutronics_code=True,
                                           )
    blanket_fluid_mat.name = 'blanket_fluid_mat'
    blanket_fluid_mat.openmc_material
    
    # Neutron Multiplier and Moderator Material
    neutron_multi_mat = nmm.Material.from_library(name='Lead')
    neutron_multi_mat.name = 'neutron_multi_mat'
    
    mod_mat = nmm.Material(
        name='Graphite',
        elements={'C':1},
        density=2.23,
        percent_type='ao',
        density_unit='g/cm3'
    )
    mod_mat.name = 'mod_mat'
    
    blanket_mod_mat = nmm.Material.from_mixture(materials=[neutron_multi_mat, mod_mat],
                            fracs=[neutron_multi, (1-neutron_multi)],
                            percent_type='vo',
                            temperature=600,
                            temperature_to_neutronics_code=True,)
    blanket_mod_mat.name = 'blanket_mod_mat'
    blanket_mod_mat.openmc_material
    
    # Reflector Materials
    blanket_ref_mat = nmm.Material(
        name='Graphite',
        elements={'C':1},
        density=2.23,
        percent_type='ao',
        density_unit='g/cm3'
    )
    blanket_ref_mat.name = 'blanket_ref_mat'
    blanket_ref_mat.openmc_material
    
    # First Wall Material
    blanket_first_wall_bp_mat = nmm.Material.from_library('Steel, Stainless 316')
    blanket_first_wall_bp_mat.name = 'blanket_first_wall_bp_mat'
    blanket_first_wall_bp_mat.openmc_material
    
    # Divertor Material
    divertor_mat = nmm.Material.from_library('Steel, Stainless 316')
    divertor_mat.name = 'divertor_mat'
    divertor_mat.openmc_material
    
    # Vaccum Vessel Material
    vac_vessel_mat = nmm.Material.from_library('Steel, Stainless 316')
    vac_vessel_mat.name = 'vac_vessel_mat'
    vac_vessel_mat.openmc_material
    
    materials = [plasma_mat,
                 blanket_fluid_mat,
                 blanket_mod_mat,
                 blanket_ref_mat,
                 blanket_first_wall_bp_mat,
                 blanket_pfc_mat,
                 blanket_heat_sink_mat,
                 divertor_mat,
                 vac_vessel_mat]
    
    return materials

# Color list : https://www.tug.org/pracjourn/2007-4/walden/color.pdf
# Make a ITER Tokamak Geometry Class
class ITERTokamak_mod(paramak.Reactor):
    """Create ITER geometry without TF Coils and PF Coils. This class modified
    from ITERTokamak function from paramak package"""
    
    def __init__(
        self,
        rotation_angle: float = 360.,
        blanket_mod_ratio: float = 0.,
    ):
        super().__init__([])
        
        self.rotation_angle = rotation_angle
        self.blanket_mod_ratio = blanket_mod_ratio
    
    def create_vessel_components(self) -> list:
        """Creates a 3d solids for each vessel component.

        Returns:
            A list of CadQuery solids: A list of 3D solid volumes
        """
        offset_r = [59, 29, 68, 25, 59]
    
        # Blanket first wall back-plate
        blanket_first_wall_bp = paramak.BlanketFP(
            plasma=self.plasma,
            thickness=5,
            start_angle=-70,
            stop_angle=230,
            rotation_angle=self.rotation_angle,
            vertical_displacement=self.plasma.vertical_displacement,
            offset_from_plasma=[[-70, 0, 90, 180, 230], [49, 19, 58, 15, 49]],
            name='blanket_first_wall_bp | SS 316',
            color=(0.6,0.7,1.0),
            stp_filename="blanket_first_wall_bp.stp",
            stl_filename="blanket_first_wall_bp.stl",
            material_tag='blanket_first_wall_bp_mat',
        )
        
        # Blanket plasma facing material
        blanket_pfc = paramak.BlanketFP(
            plasma=self.plasma,
            thickness=1,
            start_angle=-70,
            stop_angle=230,
            rotation_angle=self.rotation_angle,
            vertical_displacement=self.plasma.vertical_displacement,
            offset_from_plasma=[[-70, 0, 90, 180, 230], [46, 16, 55, 12, 46]],
            name='blanket_pfc | Beryllium',
            color=(1,0,0),
            stp_filename="blanket_pfc.stp",
            stl_filename="blanket_pfc.stl",
            material_tag='blanket_pfc_mat',
        )
        
        # Blanket heat sink
        blanket_heat_sink = paramak.BlanketFP(
            plasma=self.plasma,
            thickness=2,
            start_angle=-70,
            stop_angle=230,
            rotation_angle=self.rotation_angle,
            vertical_displacement=self.plasma.vertical_displacement,
            offset_from_plasma=[[-70, 0, 90, 180, 230], [47, 17, 56, 13, 47]],
            name='blanket_heat_sink | CuCrZr',
            color=(0.7,0.3,0),
            stp_filename="blanket_heat_sink.stp",
            stl_filename="blanket_heat_sink.stl",
            material_tag='blanket_heat_sink_mat',
        )
        
        # Front Breeder Zone
        front_breeder = paramak.BlanketFP(
            plasma=self.plasma,
            thickness=5,
            start_angle=-70,
            stop_angle=230,
            rotation_angle=self.rotation_angle,
            vertical_displacement=self.plasma.vertical_displacement,
            offset_from_plasma=[[-70, 0, 90, 180, 230], [54, 24, 63, 20, 54]],
            name='front_breeder | LiF',
            color=(0.9,0.9,0),
            stp_filename="front_breeder.stp",
            stl_filename="front_breeder.stl",
            material_tag='blanket_fluid_mat',
        )
        
        # Blanket reflector
        blanket_ref = paramak.BlanketFP(
            plasma=self.plasma,
            thickness=5,
            start_angle=-70,
            stop_angle=230,
            rotation_angle=self.rotation_angle,
            vertical_displacement=self.plasma.vertical_displacement,
            offset_from_plasma=[[-70, 0, 90, 180, 230], [99, 69, 108, 65, 99]],
            name='blanket_ref | Graphite',
            color=(0.9,0.4,0),
            stp_filename="blanket_ref.stp",
            stl_filename="blanket_ref.stl",
            material_tag='blanket_ref_mat',
        )

        # SN Divertor
        divertor = paramak.ITERtypeDivertor(
            anchors=((4.34e2, -3.3e2), (5.56e2, -3.74e2)),
            coverages=(105, 125),
            lengths=(45, 75),
            radii=(68, 65), # radii=(68, 65),
            tilts=(-43, 9), # tilts=(-30, 2),
            dome_height=45,
            dome_pos=0.45,
            rotation_angle=self.rotation_angle,
            name='divertor | SS 316',
            color=(0.3,0,0.6),
            stp_filename="divertor.stp",
            stl_filename="divertor.stl",
            material_tag='divertor_mat',
        )

        # Vacuum vessel
        divertor.points  # trigger the building of the points for divertor
        # the inner part of the vacuum vessel is computed from the outer
        # points of the blanket and the divertor
        vac_vessel_inner = paramak.RotateMixedShape(
            points=blanket_ref.outer_points + divertor.casing_points,
            rotation_angle=self.rotation_angle,
        )

        vac_vessel = paramak.RotateSplineShape(
            points=[
                (327.77, 36.5026668124882),
                (327.77, 73.37741270075162),
                (327.77, 108.31180820215741),
                (327.77, 143.2462037035632),
                (327.77, 178.18059920496898),
                (327.77, 213.11499470637477),
                (327.77, 248.04939020778068),
                (327.77, 282.98378570918646),
                (327.77, 317.9181812105922),
                (328.6121587814181, 368.23899806938385),
                (336.18303032328333, 422.4306297110355),
                (350.4835654579176, 457.5437492206628),
                (371.95910957013655, 492.47041663587777),
                (404.3208742000702, 522.0151685493631),
                (439.6516080621078, 544.4559826211985),
                (474.98234192414554, 556.3610266211815),
                (510.2245275810152, 564.0927634387052),
                (545.6438096482208, 565.1200145185009),
                (565.832800426528, 563.1864687746993),

                (580.9745435102584, 559.4390362932862),
                (616.3052773722961, 548.4109567158157),
                (651.6360112343338, 533.224020531035),
                (686.9667450963714, 515.3041214328789),
                (722.297478958409, 492.23516177329117),
                (757.6282128204466, 466.8689289401416),
                (792.9589466824843, 437.10619055069265),
                (825.7660566972336, 403.7167485984509),
                (853.525919017406, 369.42176700251196),
                (877.9209495411939, 333.90960594986575),
                (898.9511482685972, 300.5186330502012),
                (916.616515199616, 265.2383422522439),
                (932.5994662324425, 230.72194441870647),
                (946.0587934179808, 193.1122328856627),
                (956.1532888071343, 156.87835598377137),
                (962.8829523999035, 118.10702768634405),
                (967.9302000944803, 80.39197257542594),
                (968.7714080435763, 38.24754419835381),

                (968.7714080435763, 25.77097437642317),
                (964.5653682980957, -1.670738783514139),
                (956.9944967562304, -29.93883090626548),
                (956.1532888071343, -34.59540221679083),
                (946.0587934179808, -71.15339839027786),
                (931.7582582833464, -104.25874435511184),
                (914.9340993014238, -139.91477225259314),
                (898.9511482685972, -174.48160361826422),
                (883.8094051848669, -213.64300914878197),
                (867.8264541520404, -248.21908241802464),
                (851.0022951701176, -284.2078188440911),
                (834.1781361881949, -319.9470238737184),
                (818.1951851553683, -359.0978394110024),
                (800.5298182243495, -391.2313539579658),
                (776.1347877005617, -427.87174371008393),
                (744.1688856349085, -460.45530873911446),
                (708.8381517728709, -490.0255912806248),
                (673.5074179108332, -512.7040543014494),
                (638.1766840487956, -528.371873327094),
                (602.8459501867579, -539.0490644239661),
                (567.5152163247203, -546.1219131278361),
                (532.1844824626827, -548.9566889080664),
                (496.85374860064496, -547.7514325554811),
                (461.52301473860734, -541.3971156414638),
                (426.1922808765697, -527.596464992453),
                (390.8615470145321, -501.2796363633471),
                (360.57806084707124, -468.0473902249954),
                (340.389070068764, -431.4355817359209),
                (329.87397070506233, -399.072068113844),
                (327.770950832322, -357.4796824533661),
                (327.770950832322, -311.73270913617455),
                (327.770950832322, -276.79831363476876),
                (327.770950832322, -241.86391813336297),
                (327.770950832322, -206.92952263195718),
                (327.770950832322, -171.99512713055117),
                (327.770950832322, -137.06073162914538),
                (327.770950832322, -102.12633612773948),
                (327.770950832322, -67.19194062633369),

            ],
            cut=[vac_vessel_inner],  # to make a hollow shape
            rotation_angle=self.rotation_angle,
            name='vac_vessel | SS 316',
            color=(0.9,0.9,0.9),
            stp_filename='vac_vessel.stp',
            stl_filename='vac_vessel.stl',
            material_tag='vac_vessel_mat',
        )
        
        if self.blanket_mod_ratio == 0:
            
            # Blanket Fluid
            blanket_fluid = paramak.BlanketFP(
                plasma=self.plasma,
                thickness=40,
                start_angle=-70,
                stop_angle=230,
                rotation_angle=self.rotation_angle,
                vertical_displacement=self.plasma.vertical_displacement,
                offset_from_plasma=[[-70, 0, 90, 180, 230], offset_r],
                name='blanket_fluid | LIF',
                color=(0.9,0.9,0),
                stp_filename="blanket_fluid.stp",
                stl_filename="blanket_fluid.stl",
                material_tag='blanket_fluid_mat',
            )
            
            return [divertor, blanket_fluid, front_breeder, blanket_ref, blanket_heat_sink, blanket_pfc, blanket_first_wall_bp, vac_vessel, vac_vessel_inner]
            
        # Blanket Fluid
        blanket_fluid = paramak.BlanketFP(
            plasma=self.plasma,
            thickness=40*(1-self.blanket_mod_ratio),
            start_angle=-70,
            stop_angle=230,
            rotation_angle=self.rotation_angle,
            vertical_displacement=self.plasma.vertical_displacement,
            offset_from_plasma=[[-70, 0, 90, 180, 230], [x+40*(self.blanket_mod_ratio) for x in offset_r]],
            name='blanket_fluid | LiF',
            color=(0.9,0.9,0),
            stp_filename="blanket_fluid.stp",
            stl_filename="blanket_fluid.stl",
            material_tag='blanket_fluid_mat',
        )
        
        # Blanket Moderator
        blanket_mod = paramak.BlanketFP(
            plasma=self.plasma,
            thickness=40*(self.blanket_mod_ratio),
            start_angle=-70,
            stop_angle=230,
            rotation_angle=self.rotation_angle,
            vertical_displacement=self.plasma.vertical_displacement,
            offset_from_plasma=[[-70, 0, 90, 180, 230], offset_r],
            name='blanket_mod | Graphite (+ Pb)',
            color=(0.3,0.3,0),
            stp_filename="blanket_mod.stp",
            stl_filename="blanket_mod.stl",
            material_tag='blanket_mod_mat',
        )

        return [divertor, blanket_fluid, front_breeder, blanket_ref, blanket_mod, blanket_heat_sink, blanket_pfc, blanket_first_wall_bp, vac_vessel, vac_vessel_inner]
    
    
    def create_plasma(self) -> list:
        """Creates a 3d solids for the plasma.

        Returns:
            A list of CadQuery solids: A list of 3D solid volumes
        """

        self.plasma = paramak.Plasma(
            major_radius=6.2e2,
            minor_radius=200,
            elongation=1.7,
            triangularity=0.33,
            vertical_displacement=5.7e1,
            configuration="single-null",
            rotation_angle=self.rotation_angle,
            name='plasma | U235',
            color=(0.7,0,0.7),
            stp_filename='plasma.stp',
            stl_filename='plasma.stl',
            material_tag='plasma_mat',
        )

        return [self.plasma]
    
    def create_solids(self):
        """Creates a 3d solids for each component.

        Returns:
            A list of CadQuery solids: A list of 3D solid volumes
        """

        plasma = self.create_plasma()
        vessel = self.create_vessel_components()

        shapes_and_components = plasma + vessel[:-1]
        self.shapes_and_components = shapes_and_components

        return shapes_and_components
    
def create_source():
    # initialises a new source object
    source = openmc.Source()

    # the distribution of radius is just a single value
    # radius = openmc.stats.Discrete([10], [1])
    radius = openmc.stats.Discrete([420, 500, 560, 600, 620, 640, 680, 740, 820],
                                   [0.2, 0.5, 1, 1, 1, 1, 1, 0.5, 0.2])

    # the distribution of source z values is just a single value
    z_values = openmc.stats.Discrete([-200, -120, -60, -20, 0, 20, 60, 120, 200],
                                     [0.2, 0.5, 1, 1, 1, 1, 1, 0.5, 0.2])
    # z_values = openmc.stats.Discrete([-0.5, 0, 0.5], [1, 1, 1])

    # the distribution of source azimuthal angles values is a uniform distribution between 0 and 2 Pi
    angle = openmc.stats.Uniform(a=0., b=2* 3.14159265359)

    # this makes the ring source using the three distributions and a radius
    source.space = openmc.stats.CylindricalIndependent(r=radius, phi=angle, z=z_values, origin=(0.0, 0.0, 0.0))

    # sets the direction to isotropic
    source.angle = openmc.stats.Isotropic()

    # sets the energy distribution to a Muir distribution neutrons
    m_react = 5.0 # Mass of D (2) + T (3) in AMU
    kt = 36400.0 # Ion Temperature
    source.energy = openmc.stats.Muir(e0=14100000.0, m_rat=m_react, kt=kt)
    
    # Sets the source particle
    source.particle = 'neutron'
    
    return source

def create_model(batch=20, part_batch=5000, enrich_Li=0.1, mod_ratio=0, neutron_multi=0.):
    enrich_Li = enrich_Li*100
    materials = create_materials(enrich_Li, neutron_multi)
    
    if mod_ratio == 0.:
        
        geometry = ITERTokamak_mod()
        my_model = nparamak.NeutronicsModel(
            geometry = geometry,
            source = create_source(),
            simulation_batches = batch,
            simulation_particles_per_batch = part_batch,
            materials = {'plasma_mat':materials[0],
                         'divertor_mat':materials[7],
                         'blanket_fluid_mat':materials[1],
                         'blanket_ref_mat':materials[3],
                         'blanket_pfc_mat':materials[5],
                         'blanket_heat_sink_mat':materials[6],
                         'blanket_first_wall_bp_mat':materials[4],
                         'vac_vessel_mat':materials[8]},
            cell_tallies=['(n,Xt)'],
            photon_transport=False,
        )
        
        geometry.export_h5m(include_plasma=True)
        
        return my_model
        
    geometry = ITERTokamak_mod(360, mod_ratio)
    my_model = nparamak.NeutronicsModel(
        geometry = geometry,
        source = create_source(),
        simulation_batches = batch,
        simulation_particles_per_batch = part_batch,
        materials = {'plasma_mat':materials[0],
                     'divertor_mat':materials[7],
                     'blanket_fluid_mat':materials[1],
                     'blanket_ref_mat':materials[3],
                     'blanket_mod_mat':materials[2],
                     'blanket_pfc_mat':materials[5],
                     'blanket_heat_sink_mat':materials[6],
                     'blanket_first_wall_bp_mat':materials[4],
                     'vac_vessel_mat':materials[8]},
        cell_tallies=['(n,Xt)'],
        photon_transport=False,
    )
    
    geometry.export_h5m(include_plasma=True)
    
    return my_model

if __name__ == '__main__':
    # Set up command-line arguments for generating/running the model
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=int, required=True, help="Number of batch in simulation")
    parser.add_argument('--part_batch', type=int, required=True, help="Number of particle per batch")
    parser.add_argument('--enrich_Li', type=float, required=True, help="Percentage of li-6 enrichment")
    parser.add_argument('--neutron_multi', type=float, help="Percentage of neutron multiplier (Pb) in moderator")
    parser.add_argument('--mod_ratio', type=float, help="Percentage of moderator relatife to blanket fluid")
    args = parser.parse_args()
    model = create_model(args.batch, args.part_batch, args.enrich_Li, args.mod_ratio, args.neutron_multi)
    model.simulate(export_h5m=False)
    
    # open the results file
    sp = openmc.StatePoint('statepoint.' + str(args.batch) + '.h5')
    tbr_tally = sp.get_tally(scores=['(n,Xt)'])
    df = tbr_tally.get_pandas_dataframe()
    tbr_tally_result = df['mean'].sum()
    print('The tritium breeding ratio was found, TBR = ',tbr_tally_result)
