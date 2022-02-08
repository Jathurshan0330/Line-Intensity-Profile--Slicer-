import os
from pickle import TRUE
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
import logging

#
# LineIntensityProfile
#

class LineIntensityProfile(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Line Intensity Profile" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["Jathurshan Pradeepkumar (University of Moratuwa)"] # replace with "Firstname Lastname (Organization)"
    self.parent.acknowledgementText = """
This file was originally developed to fullfill the requirements of Medical Image Processing -Semester 7 module (University of Moratuwa)
""" 


# LineIntensityProfileWidget


class LineIntensityProfileWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    
    # input volume selector
    
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    
    # output volume selector
    
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.outputSelector.selectNodeUponCreation = True
    self.outputSelector.addEnabled = False
    self.outputSelector.removeEnabled = False
    self.outputSelector.noneEnabled = False
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.outputSelector)
    
    # Apply Button
    
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = True
    self.layout.addWidget(self.applyButton)
    
    # Ruler

    self.rulerSelector = slicer.qMRMLNodeComboBox()
    self.rulerSelector.nodeTypes = ["vtkMRMLAnnotationRulerNode"]
    self.rulerSelector.selectNodeUponCreation = True
    self.rulerSelector.addEnabled = False
    self.rulerSelector.removeEnabled = False
    self.rulerSelector.noneEnabled = False
    self.rulerSelector.showHidden = False
    self.rulerSelector.showChildNodeTypes = False
    self.rulerSelector.setMRMLScene( slicer.mrmlScene )
    self.rulerSelector.setToolTip( "Pick the ruler to sample along" )
    parametersFormLayout.addRow("Ruler: ", self.rulerSelector)

	
    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)

    

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = LineIntensityProfileLogic()
    print("Run the algorithm")
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), self.rulerSelector.currentNode())
   
    # Refresh Apply button state
    self.onSelect()


# LineIntensityProfileLogic


class LineIntensityProfileLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that returns true if the passed in volume node has valid image data """

    #if not volumeNode:
    #  logging.debug('hasImageData failed: no volume node')
    #  return False
    #if volumeNode.GetImageData() is None:
    #  logging.debug('hasImageData failed: no image data in volume node')
    #  return False
    return True

  def probeVolume(self,volumeNode,rulerNode):
    
    # get ruler endpoints coordinates in RAS
    p0ras=rulerNode.GetPolyData().GetPoint(0)+(1,)
    p1ras=rulerNode.GetPolyData().GetPoint(1)+(1,)
  
    # convert RAS to IJK coordinates of the vtkImageData
    ras2ijk=vtk.vtkMatrix4x4()
    volumeNode.GetRASToIJKMatrix(ras2ijk)
    p0ijk=[int(round(c)) for c in ras2ijk.MultiplyPoint(p0ras)[:3]]
    p1ijk=[int(round(c)) for c in ras2ijk.MultiplyPoint(p1ras)[:3]]
    
    # create VTK Line that will be used for sampling
    line=vtk.vtkLineSource()
    line.SetResolution(100)
    line.SetPoint1(p0ijk[0],p0ijk[1],p0ijk[2])
    line.SetPoint2(p1ijk[0],p1ijk[1],p1ijk[2])
    
    # create VTK probe filter and sample the image
    probe=vtk.vtkProbeFilter()
    probe.SetInputConnection(line.GetOutputPort())
    probe.SetSourceData(volumeNode.GetImageData())
    probe.Update()
    
    # return VTK array
    return probe.GetOutput().GetPointData().GetArray('ImageScalars')
   	

  def showChart(self, samples, names):
    print("Line Intensity Plot Initiated")
    # Switch to a layout containing a chart viewer
    lm=slicer.app.layoutManager()
    lm.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpQuantitativeView)
  
    # initialize double array MRML node for each sample list, 
    #  since this is what chart view MRML node needs
    doubleArrays=[]
    for sample in samples:
      arrayNode = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
      
      array=arrayNode.GetArray()
      nDataPoints = sample.GetNumberOfTuples()
      array.SetNumberOfTuples(nDataPoints)
      array.SetNumberOfComponents(3)
      for i in range(nDataPoints):
        array.SetComponent(i,0,i)
        array.SetComponent(i,1,sample.GetTuple1(i))
        array.SetComponent(i,2,0)
      doubleArrays.append(arrayNode)

    # get the chart view MRML node  
    cvNodes = slicer.mrmlScene.GetNodesByClass('vtkMRMLChartViewNode')
    cvNodes.SetReferenceCount(cvNodes.GetReferenceCount()-1)
    cvNodes.InitTraversal()
    cvNode=cvNodes.GetNextItemAsObject()
  
    # create a new chart node
    chartNode = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())
    for pairs in zip(names,doubleArrays):
      chartNode.AddArray(pairs[0], pairs[1].GetID())
    cvNode.SetChartNodeID(chartNode.GetID())
    return

  def run(self, volumeNode1, volumeNode2,rulerNode):
    # Run the algorithm
    print('Line Intensity Profile Logic run() called')
    
    # raise error if inputs are not initiated
    if not rulerNode or (not volumeNode1 and not volumeNode2):
      print('Initiate the Inputs - Volumes and Ruler')
      return

    # Capture screenshot
    volumeSamples1 = None
    volumeSamples2 = None
    
    if volumeNode1:
      volumeSamples1=self.probeVolume(volumeNode1, rulerNode)
    if volumeNode2:
      volumeSamples2=self.probeVolume(volumeNode2, rulerNode)
    print('volumeSamples1 = '+str(volumeSamples1))
    print('volumeSamples2 = '+str(volumeSamples2))
    
    #chart view to plot the intensity samples
    imageSamples = [volumeSamples1, volumeSamples2]
    legendNames = [volumeNode1.GetName()+' - '+rulerNode.GetName(), volumeNode2.GetName()+' - '+rulerNode.GetName()]
    self.showChart(imageSamples, legendNames)
    print('Line Intensity Profile Logic run() finished')
    return True



# Test


class LineIntensityProfileTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_LineIntensityProfile1()

  def test_LineIntensityProfile1(self):
    self.delayDisplay("Starting the test")
    
    # Sample data for testing
    import SampleData
    sampleDataLogic = SampleData.SampleDataLogic()
    volumeNode1 = sampleDataLogic.downloadMRBrainTumor1() 
    # print(volumeNode1)  
    volumeNode2 = sampleDataLogic.downloadMRBrainTumor2()
    self.delayDisplay('Test data loaded') 
    
    logic = LineIntensityProfileLogic()
    self.assertTrue(logic.hasImageData(volumeNode1))
    self.assertTrue(logic.hasImageData(volumeNode2))
    
    # initialize ruler node in a known location
    rulerNode = slicer.vtkMRMLAnnotationRulerNode()
    slicer.mrmlScene.AddNode(rulerNode)
    rulerNode.SetPosition1(75,20,0)
    rulerNode.SetPosition2(-95,20,0)
    rulerNode.SetName('Test')
    
    # initialize input selectors
    moduleWidget = slicer.modules.LineIntensityProfileWidget
    moduleWidget.rulerSelector.setCurrentNode(rulerNode)
    moduleWidget.inputSelector.setCurrentNode(volumeNode1)
    moduleWidget.outputSelector.setCurrentNode(volumeNode2)

    self.delayDisplay('Initializing')
    moduleWidget.onApplyButton()
    self.delayDisplay('If Ruler and Line intensity plot is visible : Test passed!')
