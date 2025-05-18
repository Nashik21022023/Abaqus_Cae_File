import random
tp=451.35e-6#width of platelet
h=27e-6#thikness of matrix
rho=15

#####verical dimension########
tp1=tp/2 #width of the half platelet
tp2= tp1+h #half platelet+HI
tp3=tp2+tp  #half platelet+HI+full width of the platelet
tp4=tp3+h #half+HI+full+HI
tp5=tp4+tp/2 #half+HI+full+HI+half
l=6797.25e-6  #length of the model
width=6770.25e-6/rho #width of the platelet
# Set a length of the list to 10
rho=15
#al=.2091
#a=(rho+al)*tp
#b=(rho-al)*tp
#for i in range(0, 27):
    # any random float between a to b
    # don't use round() if you need number as it is
    #lp1 = random.uniform(a, b)
    #lp.append(lp1)
from abaqus import * 
from abaqusConstants import *
import __main__
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=121.633964538574, 
    height=118.363288879395)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
Mdb()

#dimensions from the origin of the cs (horizontal dimension)########
first1=5077.6875e-6 #first length(bottom left)
first2=first1+h  #bottom left+junction
first3=l #full bottom
second1=1692.5625e-6 #middle left
second2=second1+h #middle left+junction
second3=l #full middle
third1=5077.6875e-6 #top left
third2=third1+h #top left+junction
third3=l #full top
###################################space addded-rectangle######################
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
     sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.rectangle(point1=(0,0), point2=(l,tp5)) #Length*width
p = mdb.models['Model-1'].Part(name='RVE', dimensionality=TWO_D_PLANAR, ########################Part-8-------->RVE
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['RVE'] ##########part-8---> RVE
p.BaseShell(sketch=s1)
s1.unsetPrimaryObject()
#########################sapce added###########################
p = mdb.models['Model-1'].parts['RVE']   ########################Part-8-------->RVE
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
p = mdb.models['Model-1'].parts['RVE']  #################
f, e, d1 = p.faces, p.edges, p.datums
# t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(
#     -12.5, 13.125, 0.0))
#########################sapce added-partitioning###########################
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=179.46, gridSpacing=4.48)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['RVE'] ########################Part-8-------->RVE
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
##first row platelet
s.rectangle(point1=(0, 0), point2=(first1, tp1)) #bottom left platelet
s.rectangle(point1=(first2, 0), point2=(first3, tp1)) ###bottom right platelet
##second row platelet
s.rectangle(point1=(0, tp2), point2=(second1, tp3)) #middle left
s.rectangle(point1=(second2, tp2), point2=(second3, tp3)) #middle right
##third row of platelet
s.rectangle(point1=(0.0, tp4), point2=(third1, tp5)) #top left
s.rectangle(point1=(third2, tp4), point2=(third3, tp5)) #top right
# ##first interface
s.rectangle(point1=(0.0, tp1), point2=(second3, tp2)) ######HI bottom
# s.rectangle(point1=(second2, tp1), point2=(first1, tp2))
# s.rectangle(point1=(first2, tp1), point2=(second3, tp2))
# ##second interface 
s.rectangle(point1=(0, tp3), point2=(second3, tp4))       ####HI top
# s.rectangle(point1=(second2, tp3), point2=(third1, tp4))
# s.rectangle(point1=(third2, tp3), point2=(second3, tp4))
# ##vertical interface
# s.rectangle(point1=(first1, 0), point2=(first2, tp2))
# s.rectangle(point1=(second1, tp1), point2=(second2, tp4))
# s.rectangle(point1=(third1, tp3), point2=(third2, tp5))

p = mdb.models['Model-1'].parts['RVE']       ########################Part-8-------->RVE
f = p.faces
pickedFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
e1, d2 = p.edges, p.datums
p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
# s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=4.61, 
#     gridSpacing=0.11)
# g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
# s.setPrimaryObject(option=SUPERIMPOSE)
# p = mdb.models['Model-1'].parts['Part-8']
# p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
# session.viewports['Viewport: 1'].view.setValues(nearPlane=4.59797, 
#     farPlane=4.6333, width=0.116715, height=0.0593887, cameraPosition=(
#     0.501434, 0.0206288, 4.61563), cameraTarget=(0.501434, 0.0206288, 0))

# s.rectangle(point1=(first1, 0), point2=(first2, tp2))
# s.rectangle(point1=(second1, tp1), point2=(second2, tp4))
# s.rectangle(point1=(third1, tp3), point2=(third2, tp5))
# p = mdb.models['Model-1'].parts['Part-8']
# p.Cut(sketch=s)
# s.unsetPrimaryObject()
# del mdb.models['Model-1'].sketches['__profile__']
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0174691, 
    farPlane=0.0189486, width=0.00490125, height=0.00237889, 
    viewOffsetX=0.000244146, viewOffsetY=0.000115928)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='Platelet')
mdb.models['Model-1'].materials['Platelet'].Elastic(table=((100000.0, 0.2), ))
mdb.models['Model-1'].Material(name='Matrix')
mdb.models['Model-1'].materials['Matrix'].Elastic(type=TRACTION, table=((136.0, 
    68.0, 68.0), ))
mdb.models['Model-1'].materials['Matrix'].QuadsDamageInitiation(table=((1.76, 
    1.76, 1.76), ))
mdb.models['Model-1'].materials['Matrix'].quadsDamageInitiation.DamageEvolution(
    type=DISPLACEMENT, softening=TABULAR, table=((0.0, 0.0), (0.112343312, 
    1.04e-07), (0.201993954, 2.08e-07), (0.275196878, 3.11e-07), (
    0.33609812, 4.15e-07), (0.38755825, 5.19e-07), (0.43161473, 6.23e-07), 
    (0.469758099, 7.26e-07), (0.503103949, 8.3e-07), (0.532503844, 
    9.34e-07), (0.558619071, 1.04e-06), (0.58197097, 1.14e-06), (
    0.602976096, 1.25e-06), (0.621971286, 1.35e-06), (0.639231857, 
    1.45e-06), (0.654985039, 1.56e-06), (0.669420035, 1.66e-06), (
    0.682695653, 1.76e-06), (0.694946177, 1.87e-06), (0.706285926, 
    1.97e-06), (0.716812827, 2.08e-06), (0.726611254, 2.18e-06), (
    0.735754297, 2.28e-06), (0.744305582, 2.39e-06), (0.752320758, 
    2.49e-06), (0.759848708, 2.59e-06), (0.766932548, 2.7e-06), (
    0.773610453, 2.8e-06), (0.779916342, 2.91e-06), (0.785880461, 
    3.01e-06), (0.791529861, 3.11e-06), (0.796888814, 3.22e-06), (
    0.801979155, 3.32e-06), (0.806820588, 3.42e-06), (0.811430934, 
    3.53e-06), (0.815826352, 3.63e-06), (0.820021528, 3.74e-06), (
    0.824029843, 3.84e-06), (0.827863508, 3.94e-06), (0.831533695, 
    4.05e-06), (0.835050642, 4.15e-06), (0.838423751, 4.26e-06), (
    0.841661668, 4.36e-06), (0.844772362, 4.46e-06), (0.847763187, 
    4.57e-06), (0.850640939, 4.67e-06), (0.853411913, 4.77e-06), (
    0.856081943, 4.88e-06), (0.858656447, 4.98e-06), (0.86114046, 
    5.09e-06), (0.925390081, 1.02e-05), (0.948991473, 1.53e-05), (
    0.961249453, 2.03e-05), (0.968757429, 2.54e-05), (0.973828245, 
    3.05e-05), (0.97748288, 3.56e-05), (0.980241908, 4.07e-05), (
    0.98239861, 4.58e-05), (0.984130817, 5.09e-05), (0.985552628, 
    5.59e-05), (0.986740612, 6.1e-05), (0.987748068, 6.61e-05), (
    0.988613241, 7.12e-05), (0.989364285, 7.63e-05), (0.990022385, 
    8.14e-05), (0.990603788, 8.64e-05), (0.991121165, 9.15e-05), (
    0.99158454, 9.66e-05), (0.992001947, 0.000101705), (0.992379905, 
    0.00010679), (0.992723753, 0.000111875), (0.993037909, 0.000116961), (
    0.99332606, 0.000122046), (0.993591307, 0.000127131), (0.993836275, 
    0.000132216), (0.994063206, 0.000137302), (0.994274021, 0.000142387), (
    0.994470376, 0.000147472), (0.994653712, 0.000152557), (0.99482528, 
    0.000157643), (0.994986179, 0.000162728), (0.995137374, 0.000167813), (
    0.995279718, 0.000172898), (0.995413965, 0.000177984), (0.995540786, 
    0.000183069), (0.995660783, 0.000188154), (0.99577449, 0.000193239), (
    0.99588239, 0.000198325), (0.995984917, 0.00020341), (0.996082462, 
    0.000208495), (0.99617538, 0.00021358), (0.996263993, 0.000218666), (
    0.996348592, 0.000223751), (0.996429445, 0.000228836), (0.996506794, 
    0.000233921), (0.996580864, 0.000239007), (0.996651857, 0.000244092), (
    0.996726512, 0.000249469), (0.996729781, 0.000249615), (0.996733047, 
    0.00024976), (0.996736308, 0.000249906), (0.996739566, 0.000250052), (
    0.99674282, 0.000250198), (0.99674607, 0.000250343), (0.996749317, 
    0.000250489), (0.996752559, 0.000250635), (0.996755798, 0.000250781), (
    0.996759033, 0.000250926), (0.996762265, 0.000251072), (0.996765492, 
    0.000251218), (0.996768716, 0.000251364), (0.996771936, 0.00025151), (
    0.996775153, 0.000251655), (0.996778366, 0.000251801), (0.996781575, 
    0.000251947), (0.99678478, 0.000252093), (0.996787982, 0.000252238), (
    0.99679118, 0.000252384), (0.996794374, 0.00025253), (0.996797565, 
    0.000252676), (0.996800752, 0.000252821), (0.996803935, 0.000252967), (
    0.996807115, 0.000253113), (0.996810291, 0.000253259), (0.996813463, 
    0.000253405), (0.996816632, 0.00025355), (0.996819797, 0.000253696), (
    0.996822958, 0.000253842), (0.996826116, 0.000253988), (0.99682927, 
    0.000254133), (0.996832421, 0.000254279), (0.996835568, 0.000254425), (
    0.996838711, 0.000254571), (0.996841851, 0.000254716), (0.996844988, 
    0.000254862), (0.99684812, 0.000255008), (0.996851249, 0.000255154), (
    0.996854375, 0.0002553), (0.996857497, 0.000255445), (0.996860615, 
    0.000255591), (0.99686373, 0.000255737), (0.996866842, 0.000255883), (
    0.99686995, 0.000256028), (0.996873054, 0.000256174), (0.996876155, 
    0.00025632), (0.997023904, 0.000263463), (0.997163877, 0.000270606), (
    0.997296672, 0.000277748), (0.997422828, 0.000284891), (0.997542829, 
    0.000292034), (0.997657116, 0.000299177), (0.997766087, 0.000306319), (
    0.997870106, 0.000313462), (0.997969501, 0.000320605), (0.998064574, 
    0.000327748), (0.998155602, 0.000334891), (0.998242837, 0.000342033), (
    0.998326511, 0.000349176), (0.998406839, 0.000356319), (0.998484016, 
    0.000363462), (0.998558225, 0.000370604), (0.998629634, 0.000377747), (
    0.998698398, 0.00038489), (0.998764661, 0.000392033), (0.998828558, 
    0.000399176), (0.998890213, 0.000406318), (0.998949742, 0.000413461), (
    0.999007253, 0.000420604), (0.999062846, 0.000427747), (0.999116618, 
    0.000434889), (0.999168654, 0.000442032), (0.999219039, 0.000449175), (
    0.999267849, 0.000456318), (0.999315157, 0.00046346), (0.999361032, 
    0.000470603), (0.999405537, 0.000477746), (0.999448733, 0.000484889), (
    0.999490677, 0.000492032), (0.999531423, 0.000499174), (0.999571021, 
    0.000506317), (0.999609519, 0.00051346), (0.999646963, 0.000520603), (
    0.999683394, 0.000527745), (0.999718854, 0.000534888), (0.999753381, 
    0.000542031), (0.999787011, 0.000549174), (0.999819778, 0.000556317), (
    0.999851716, 0.000563459), (0.999882856, 0.000570602), (0.999913227, 
    0.000577745), (0.999942856, 0.000584888), (0.999971772, 0.00059203), (
    1.0, 0.000599173)))
mdb.models['Model-1'].HomogeneousSolidSection(name='Platelet', 
    material='Platelet', thickness=None)
mdb.models['Model-1'].CohesiveSection(name='Section-2', material='Matrix', 
    response=TRACTION_SEPARATION, initialThicknessType=SPECIFY, 
    initialThickness=2.7e-05, outOfPlaneThickness=1.0)
session.viewports['Viewport: 1'].view.fitView()
mdb.models['Model-1'].sections.changeKey(fromName='Section-2', toName='Matrix')
# p = mdb.models['Model-1'].parts['RVE'] ########################Part-8-------->RVE
# f = p.faces
# faces = f.getSequenceFromMask(mask=('[#2a83 ]', ), )
# region = p.Set(faces=faces, name='Set-1')
# p = mdb.models['Model-1'].parts['RVE']
# p.SectionAssignment(region=region, sectionName='Platelet', offset=0.0, 
#     offsetType=MIDDLE_SURFACE, offsetField='', 
#     thicknessAssignment=FROM_SECTION)
    
# session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0169829, 
#     farPlane=0.0194347, width=0.00909649, height=0.00441511, 
#     viewOffsetX=-0.000115711, viewOffsetY=0.00113966)
# p = mdb.models['Model-1'].parts['RVE'] ########################Part-8-------->RVE
# f = p.faces
# faces = f.getSequenceFromMask(mask=('[#557c ]', ), )
# region = p.Set(faces=faces, name='Set-2')
# p = mdb.models['Model-1'].parts['RVE'] ########################Part-8-------->RVE
# p.SectionAssignment(region=region, sectionName='Matrix', offset=0.0, 
#     offsetType=MIDDLE_SURFACE, offsetField='', 
#     thicknessAssignment=FROM_SECTION)

##########Section assignment##############
p = mdb.models['Model-1'].parts['RVE']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#2b5 ]', ), )
region = p.Set(faces=faces, name='platelets')
p = mdb.models['Model-1'].parts['RVE']
p.SectionAssignment(region=region, sectionName='Platelet', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['Model-1'].parts['RVE']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#54a ]', ), )
region = p.Set(faces=faces, name='matrix')
p = mdb.models['Model-1'].parts['RVE']
p.SectionAssignment(region=region, sectionName='Matrix', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)


########assembly module#######33
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['RVE'] ########################Part-8-------->RVE
a.Instance(name='RVE-1', part=p, dependent=ON) ########################Part-8-------->RVE
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0179424, 
    farPlane=0.0184752, width=0.0017623, height=0.00085536, 
    viewOffsetX=-0.000898793, viewOffsetY=0.000116928)
session.viewports['Viewport: 1'].view.fitView()


#############step module#############
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial', 
    maxNumInc=1000, initialInc=0.01, minInc=1e-15, maxInc=0.1, nlgeom=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
mdb.models['Model-1'].FieldOutputRequest(name='F-Output-2', 
    createStepName='Step-1', variables=('S', 'E', 'U', 'RF', 'SDEG'))
regionDef=mdb.models['Model-1'].rootAssembly.sets['Master_R_D']
mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-2', 
    createStepName='Step-1', variables=('U1', 'RF1'), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

#########Mesh and node set#########
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0180878, 
    farPlane=0.0183298, width=0.000701192, height=0.000288777, 
    viewOffsetX=-0.00418267, viewOffsetY=0.00026906)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0179654, 
    farPlane=0.0184522, width=0.00155917, height=0.000642124, 
    viewOffsetX=-0.00372912, viewOffsetY=-0.000223586)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0178582, 
    farPlane=0.0185594, width=0.00224661, height=0.000925238, 
    viewOffsetX=-0.00134345, viewOffsetY=0.000317203)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0177885, 
    farPlane=0.0186291, width=0.00269429, height=0.00110961, 
    viewOffsetX=-0.00125668, viewOffsetY=-0.000188266)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0178364, 
    farPlane=0.0185813, width=0.00238708, height=0.000983089, 
    viewOffsetX=0.00200003, viewOffsetY=6.52021e-005)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0179334, 
    farPlane=0.0184843, width=0.00199345, height=0.000820979, 
    viewOffsetX=0.00357181, viewOffsetY=9.46153e-005)
session.viewports['Viewport: 1'].view.fitView()
p = mdb.models['Model-1'].parts['RVE']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#4e9fd79f #3 ]', ), )
p.seedEdgeBySize(edges=pickedEdges, size=2.7e-05, deviationFactor=0.1, 
        constraint=FINER)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0180062, 
    farPlane=0.0184115, width=0.00129796, height=0.000534548, 
    viewOffsetX=-0.00389345, viewOffsetY=0.000316285)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0179654, 
    farPlane=0.0184522, width=0.00155917, height=0.000642124, 
    viewOffsetX=-0.00375427, viewOffsetY=-0.000236384)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0179166, 
    farPlane=0.018501, width=0.0018721, height=0.000771, 
    viewOffsetX=-0.00139808, viewOffsetY=0.000285217)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0180182, 
    farPlane=0.0183994, width=0.0012209, height=0.000502811, 
    viewOffsetX=-0.00155246, viewOffsetY=-0.00026135)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0178983, 
    farPlane=0.0185193, width=0.00198956, height=0.000819375, 
    viewOffsetX=0.00213675, viewOffsetY=9.45874e-009)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0179166, 
    farPlane=0.018501, width=0.0018721, height=0.000771, 
    viewOffsetX=0.00355529, viewOffsetY=5.45808e-005)
session.viewports['Viewport: 1'].view.fitView()
p = mdb.models['Model-1'].parts['RVE']
e = p.edges
pickedEdges = e.getSequenceFromMask(mask=('[#b1602860 ]', ), )
p.seedEdgeByNumber(edges=pickedEdges, number=1, constraint=FINER)
p = mdb.models['Model-1'].parts['RVE']
f = p.faces
pickedRegions = f.getSequenceFromMask(mask=('[#2b5 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=STRUCTURED)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0178789, 
    farPlane=0.0185387, width=0.00211425, height=0.000870728, 
    viewOffsetX=-0.0013947, viewOffsetY=0.000162937)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0178582, 
    farPlane=0.0185594, width=0.00224661, height=0.000925238, 
    viewOffsetX=-0.00135441, viewOffsetY=-0.000398182)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0178364, 
    farPlane=0.0185813, width=0.00238708, height=0.000983089, 
    viewOffsetX=0.00332371, viewOffsetY=0.000141879)
p = mdb.models['Model-1'].parts['RVE']
f = p.faces
pickedRegions = f.getSequenceFromMask(mask=('[#54a ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=SWEEP)
p = mdb.models['Model-1'].parts['RVE']
f, e = p.faces, p.edges
p.setSweepPath(region=f[1], edge=e[6], sense=REVERSE)
p = mdb.models['Model-1'].parts['RVE']
f1, e1 = p.faces, p.edges
p.setSweepPath(region=f1[3], edge=e1[13], sense=REVERSE)
p = mdb.models['Model-1'].parts['RVE']
f, e = p.faces, p.edges
p.setSweepPath(region=f[6], edge=e[21], sense=REVERSE)
p = mdb.models['Model-1'].parts['RVE']
f1, e1 = p.faces, p.edges
p.setSweepPath(region=f1[8], edge=e1[28], sense=REVERSE)
p = mdb.models['Model-1'].parts['RVE']
f, e = p.faces, p.edges
p.setSweepPath(region=f[10], edge=e[29], sense=REVERSE)
session.viewports['Viewport: 1'].view.fitView()
elemType1 = mesh.ElemType(elemCode=CPE4R, elemLibrary=STANDARD, 
    secondOrderAccuracy=OFF, hourglassControl=DEFAULT, 
    distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=CPE3, elemLibrary=STANDARD)
p = mdb.models['Model-1'].parts['RVE']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#2b5 ]', ), )
pickedRegions =(faces, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
elemType1 = mesh.ElemType(elemCode=COH2D4, elemLibrary=STANDARD)
elemType2 = mesh.ElemType(elemCode=UNKNOWN_TRI, elemLibrary=STANDARD)
p = mdb.models['Model-1'].parts['RVE']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#54a ]', ), )
pickedRegions =(faces, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
p = mdb.models['Model-1'].parts['RVE']
p.generateMesh()
a1 = mdb.models['Model-1'].rootAssembly
a1.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0178373, 
    farPlane=0.0185804, width=0.0023872, height=0.000980706, 
    viewOffsetX=-0.00333521, viewOffsetY=0.000315484)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0178373, 
    farPlane=0.0185804, width=0.0023872, height=0.000980706, 
    viewOffsetX=0.0033264, viewOffsetY=0.000282017)
session.viewports['Viewport: 1'].view.fitView()
a1 = mdb.models['Model-1'].rootAssembly
n1 = a1.instances['RVE-1'].nodes
nodes1 = n1.getSequenceFromMask(mask=(
    '[#800000a6 #ffffffff:3 #3 #0:10 #fffffff8 #ffffffff:6 #fff ]', ), )
a1.Set(nodes=nodes1, name='Top')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0178591, 
    farPlane=0.0185585, width=0.00224672, height=0.000922992, 
    viewOffsetX=-0.00338783, viewOffsetY=-0.00032949)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0177895, 
    farPlane=0.0186281, width=0.00269444, height=0.00110693, 
    viewOffsetX=0.00320597, viewOffsetY=-0.000342348)
session.viewports['Viewport: 1'].view.fitView()
a1 = mdb.models['Model-1'].rootAssembly
n1 = a1.instances['RVE-1'].nodes
nodes1 = n1.getSequenceFromMask(mask=(
    '[#6600 #0:25 #fffffff0 #ffffffff:9 #ffff ]', ), )
a1.Set(nodes=nodes1, name='Bottom')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0176425, 
    farPlane=0.0187751, width=0.00364104, height=0.00149581, 
    viewOffsetX=-0.00269111, viewOffsetY=1.02984e-005)
a1 = mdb.models['Model-1'].rootAssembly
n1 = a1.instances['RVE-1'].nodes
nodes1 = n1.getSequenceFromMask(mask=(
    '[#811008 #0:3 #1fc #0:20 #e0000000 #f #0:39', ' #ffff00 ]', ), )
a1.Set(nodes=nodes1, name='Left')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0174901, 
    farPlane=0.0189275, width=0.00462324, height=0.00189931, 
    viewOffsetX=0.00220482, viewOffsetY=0.000157615)
a1 = mdb.models['Model-1'].rootAssembly
n1 = a1.instances['RVE-1'].nodes
nodes1 = n1.getSequenceFromMask(mask=(
    '[#288040 #0:13 #f0000000 #7 #0:20 #7f0000 #0:19', ' #3fffc000 ]', ), )
a1.Set(nodes=nodes1, name='Right')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].view.fitView()
