targetScope = 'resourceGroup'

@description('Draft output generated from architecture IR. Not deployment-ready without review.')
param location string = resourceGroup().location

@description('Draft architecture resources extracted from source diagrams.')
var inferredResources = [
  {
    symbolicName: 'resource_1'
    name: 'resource-1'
    id: 'ev-e2a4c88a41c47cf9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_2'
    name: 'resource-2'
    id: 'ev-ed92313deac11960'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'ENTERPRISE_AZURE_DEVOPS_AUTOMATION'
    name: 'ENTERPRISE--AZURE--DEVOPS-AUTOMATION'
    id: 'ev-a6b2ceb5d70c14eb'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram--to-IaC-Compiler'
    id: 'ev-6eb7cfca153ab386'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Azure_Bicep_Terraform'
    name: '---Azure-BicepTerraform----'
    id: 'ev-d75715e51f99c0a2'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_6'
    name: 'resource-6'
    id: 'ev-e7bbd27415313083'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'diagram_draw_io_PPTX'
    name: '---diagram--drawio--PPTX'
    id: 'ev-f37f516dcc2283f7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_8'
    name: 'resource-8'
    id: 'ev-80832789e09e270c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'AI_understanding_IR'
    name: 'AI----understanding--IR'
    id: 'ev-bfd5f1f4d71ab858'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_10'
    name: 'resource-10'
    id: 'ev-cb1db3b6c4035827'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IaC_Bicep_Terraform'
    name: 'IaC---Bicep--Terraform'
    id: 'ev-addd063f8f36ff9d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_2026_Architecture_Diagram_Understanding_Engine'
    name: '2026--Architecture-Diagram-Understanding-Engine'
    id: 'ev-c25a6d3808371d64'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_13'
    name: 'resource-13'
    id: 'ev-ddfc1d3819167850'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_14'
    name: 'resource-14'
    id: 'ev-e72bc9edb9af42b3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_02_PROBLEM_DEFINITION'
    name: '02--PROBLEM-DEFINITION'
    id: 'ev-8f958d83277b58c6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_16'
    name: '-'
    id: 'ev-3f465fa849a1dc4c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_17'
    name: 'resource-17'
    id: 'ev-d67160c27a1e5e26'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_18'
    name: 'resource-18'
    id: 'ev-64992b0d5c04e2c9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IaC'
    name: '------IaC--'
    id: 'ev-9cd0884f3089d3a3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_20'
    name: 'resource-20'
    id: 'ev-38f995ea5e930b70'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_21'
    name: 'resource-21'
    id: 'ev-26ca855c0710855f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_22'
    name: '--'
    id: 'ev-d06da05cdcf7afe9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'PowerPoint_draw_io_PDF'
    name: 'PowerPoint--drawio--PDF------'
    id: 'ev-cd6706bd41128bb8'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_24'
    name: 'resource-24'
    id: 'ev-d1d57a724b74e884'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_25'
    name: 'resource-25'
    id: 'ev-9eae2f6830dd99c5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_26'
    name: '--'
    id: 'ev-da0f5ca23165009d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IaC'
    name: '---IaC---'
    id: 'ev-a8ca7f73472992f4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_28'
    name: 'resource-28'
    id: 'ev-efee66efc49fb67e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_29'
    name: 'resource-29'
    id: 'ev-ebf2d9712bd32072'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_30'
    name: '-'
    id: 'ev-6ee560530731e4b4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Bicep_Terraform'
    name: 'BicepTerraform-------'
    id: 'ev-a0f4c4b62c417471'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_32'
    name: 'resource-32'
    id: 'ev-40f89bcd2411726c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_33'
    name: 'resource-33'
    id: 'ev-57189195dd5474b6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_34'
    name: '--'
    id: 'ev-d2a29e5d43ef4dcb'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'SKU_CIDR'
    name: '-SKUCIDR------'
    id: 'ev-5b21325a94448a0c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-bcbce913506c8950'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_02_17'
    name: '02---17'
    id: 'ev-69367aab1255c466'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_38'
    name: 'resource-38'
    id: 'ev-d3e874c846e26415'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_39'
    name: 'resource-39'
    id: 'ev-be0a3dd925fab1bf'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_03_KEY_INSIGHT'
    name: '03--KEY-INSIGHT'
    id: 'ev-ef784ea89ade479e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_41'
    name: '-'
    id: 'ev-0605aa08e493f578'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_42'
    name: 'resource-42'
    id: 'ev-bd16cd0253e1e725'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_43'
    name: 'resource-43'
    id: 'ev-2a528764790c507e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_44'
    name: '---------'
    id: 'ev-5aed382874d06b29'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_6'
    name: '--------6------'
    id: 'ev-3314c6c139e29da3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_46'
    name: 'resource-46'
    id: 'ev-5d0e3ff5036f256b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_47'
    name: '--'
    id: 'ev-92c04b84fb3bb8b3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'shape_metadata'
    name: 'shape-metadata'
    id: 'ev-4b18b2606c7ed4e4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_49'
    name: 'resource-49'
    id: 'ev-ac8abae6dec74b96'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_50'
    name: '-'
    id: 'ev-4695597240ee5ba1'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'visual_layout'
    name: 'visual-layout'
    id: 'ev-3027640f7481d696'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_52'
    name: 'resource-52'
    id: 'ev-7dd0da1dfbb4cc0b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'OCR'
    name: 'OCR'
    id: 'ev-bd7a69324c4dc7c6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'text_label'
    name: 'text--label'
    id: 'ev-b2158c5943c148b1'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_55'
    name: 'resource-55'
    id: 'ev-52e6cba79e5bd038'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_56'
    name: '-'
    id: 'ev-b3c2cf21a8d93962'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Azure_resource'
    name: 'Azure-resource'
    id: 'ev-119cf002bb775092'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_58'
    name: 'resource-58'
    id: 'ev-c2a65cb837657938'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'LLM_Reasoning'
    name: 'LLM-Reasoning'
    id: 'ev-6b2d425c8eb1e9b1'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'semantic'
    name: 'semantic'
    id: 'ev-7ab3913f55bfcc98'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_61'
    name: 'resource-61'
    id: 'ev-0fbe96882bce661d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Self_Ensemble'
    name: 'Self-Ensemble'
    id: 'ev-a4f961578d07f6b4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'confidence_merge'
    name: 'confidence-merge'
    id: 'ev-16c92eaa23256f12'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_6_signals_1_Architecture_Understanding_Engine'
    name: '6-signals--1-Architecture-Understanding-Engine'
    id: 'ev-20194b1e1e0d1398'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-6208b434ca6eb94e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_03_17'
    name: '03---17'
    id: 'ev-a5b69a17a0698bfc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_67'
    name: 'resource-67'
    id: 'ev-97dd4242e290ade5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_68'
    name: 'resource-68'
    id: 'ev-0c73324d378d4747'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_04_WORKFLOW'
    name: '04--WORKFLOW'
    id: 'ev-94ffeb786db13a5a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Multi_Stage_Architecture_Understanding_Workflow'
    name: 'Multi-Stage-Architecture-Understanding-Workflow'
    id: 'ev-eceaff7c52a752f3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_71'
    name: 'resource-71'
    id: 'ev-de7160a40eb9223f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_1'
    name: '1'
    id: 'ev-8d88d8a5cbea7778'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Input_Files'
    name: 'Input-Files'
    id: 'ev-556fa3952356eba3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_74'
    name: 'resource-74'
    id: 'ev-1dc24dbc285f24c0'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_2'
    name: '2'
    id: 'ev-5fc729aa7775f648'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Multi_Extractor'
    name: 'Multi-Extractor'
    id: 'ev-101ce9d644c726b2'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_77'
    name: 'resource-77'
    id: 'ev-86f2aa8abe74e4ed'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_3'
    name: '3'
    id: 'ev-9b9c59e7d5f40a9c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Element_Registry'
    name: 'Element-Registry'
    id: 'ev-71edcf2d343084bf'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_80'
    name: 'resource-80'
    id: 'ev-22f7448237e4d4c8'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_4'
    name: '4'
    id: 'ev-43d26d357ccb054b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Graph_Reconstruction'
    name: 'Graph-Reconstruction'
    id: 'ev-3a61df9582d50494'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_83'
    name: 'resource-83'
    id: 'ev-5149950fac6a6cbe'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_5'
    name: '5'
    id: 'ev-89d21ce030230074'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_IR'
    name: 'Architecture-IR'
    id: 'ev-379fc77495cdc911'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_86'
    name: 'resource-86'
    id: 'ev-516e77d45158cbfc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_6'
    name: '6'
    id: 'ev-a9789bf0b61362cc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IaC_Generator'
    name: 'IaC-Generator'
    id: 'ev-702ad9ca95500d26'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_89'
    name: 'resource-89'
    id: 'ev-1b4db8aa98fa02e9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_7'
    name: '7'
    id: 'ev-b601b4a18aff5358'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Validation_What_if'
    name: 'Validation--What-if'
    id: 'ev-45a98f96cdedf75a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'OUTPUTS'
    name: 'OUTPUTS'
    id: 'ev-10f715d534504b3f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_93'
    name: 'resource-93'
    id: 'ev-94af7ef7e28faebc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Bicep'
    name: 'Bicep'
    id: 'ev-a9cc395f52156f2a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_95'
    name: 'resource-95'
    id: 'ev-578ae614d29a5aaa'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Terraform'
    name: 'Terraform'
    id: 'ev-251cc5e33f8e50bb'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_97'
    name: 'resource-97'
    id: 'ev-ca9b20ad9698e4a4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Validation_Report'
    name: 'Validation-Report'
    id: 'ev-6b5377d47403e561'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_99'
    name: 'resource-99'
    id: 'ev-e90625f48d321c5f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Missing_Questions'
    name: 'Missing-Questions'
    id: 'ev-053364081ccf1d13'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_101'
    name: 'resource-101'
    id: 'ev-c1a8ba179fdd963d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Review'
    name: 'Architecture-Review'
    id: 'ev-683ba269d7eb294e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-f7b395e027c1068b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_04_17'
    name: '04---17'
    id: 'ev-243585c9eba7c095'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_105'
    name: 'resource-105'
    id: 'ev-ae0b0374064523e0'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_106'
    name: 'resource-106'
    id: 'ev-fbde41f8883158a5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_05_VLM_STRATEGY'
    name: '05--VLM-STRATEGY'
    id: 'ev-ea3de8ea42e147b9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'VLM_Reconciliation_Engine'
    name: 'VLM----Reconciliation-Engine'
    id: 'ev-e45c76a11f5cdec9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_109'
    name: 'resource-109'
    id: 'ev-b98eaa1279601d5b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_110'
    name: 'resource-110'
    id: 'ev-753285ede1f31d1e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_1'
    name: '1'
    id: 'ev-49d8ad23a31fe75a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Full_slide_VLM'
    name: 'Full-slide-VLM----'
    id: 'ev-6e934c108afc1e99'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_113'
    name: 'resource-113'
    id: 'ev-88df3c0b350c460d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_114'
    name: 'resource-114'
    id: 'ev-533902aa8fdb3800'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_2'
    name: '2'
    id: 'ev-9271f02c7a3e1fee'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Tile_Crop_VLM'
    name: 'Tile--Crop-VLM----'
    id: 'ev-e783e85f949efaed'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_117'
    name: 'resource-117'
    id: 'ev-527a5a983bd083ef'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_118'
    name: 'resource-118'
    id: 'ev-8c0c6b8c649f7a2c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_3'
    name: '3'
    id: 'ev-9df26ce2dcab0b9d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'OCR'
    name: 'OCR-----'
    id: 'ev-c86a1847ab7e3719'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_121'
    name: 'resource-121'
    id: 'ev-72895c21330f19b4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_122'
    name: 'resource-122'
    id: 'ev-808d6bce36389382'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_4'
    name: '4'
    id: 'ev-5ae69cbea5c5261e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Azure'
    name: 'Azure-------'
    id: 'ev-79b5d0e5cc3a93f7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_125'
    name: 'resource-125'
    id: 'ev-957708e8d6c3348a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_126'
    name: 'resource-126'
    id: 'ev-4f36d5dff4e18da5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_5'
    name: '5'
    id: 'ev-c5b7991fccb16809'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'edge_boundary'
    name: '------edge--boundary'
    id: 'ev-d385985c05b16a39'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_129'
    name: 'resource-129'
    id: 'ev-bd6caefdc037b3c0'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_130'
    name: 'resource-130'
    id: 'ev-f40f6c83f72d09f2'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_6'
    name: '6'
    id: 'ev-9a67d2d37b41d695'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Graph_reconciled_output'
    name: '-Architecture-Graph---reconciled-output'
    id: 'ev-67ff09f5d58945d9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_133'
    name: 'resource-133'
    id: 'ev-38fbb44d8b75b83c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'VLM_Reconciliation'
    name: 'VLM--Reconciliation'
    id: 'ev-7cbc88cd96c6a8ed'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_135'
    name: '-----'
    id: 'ev-c9ebf808e829bb47'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-def548715a59fe18'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_05_17'
    name: '05---17'
    id: 'ev-bfaa62f36ecfa898'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_138'
    name: 'resource-138'
    id: 'ev-1ef91e1a18ac9006'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_139'
    name: 'resource-139'
    id: 'ev-4d866af59abba1cb'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_06_RESEARCH_INSPIRED_DESIGN_PRINCIPLES'
    name: '06--RESEARCH-INSPIRED-DESIGN-PRINCIPLES'
    id: 'ev-2bd11f77ffd2493c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Research_Inspired_Design_Principles'
    name: 'Research-Inspired-Design-Principles'
    id: 'ev-faad14ddb89f2b53'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_142'
    name: 'resource-142'
    id: 'ev-7cc2094f7d3eecb3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_143'
    name: 'resource-143'
    id: 'ev-8ff3bd86606ac63b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Editable_source'
    name: 'Editable-source--'
    id: 'ev-ebbd478b8f7a2849'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'PPTX_draw_io_shape_metadata'
    name: 'PPTX--drawio-shape-metadata--'
    id: 'ev-4cc61d10faeba673'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_146'
    name: 'resource-146'
    id: 'ev-8f6d3ac82f23d582'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_147'
    name: 'resource-147'
    id: 'ev-2210a15d0c2d50aa'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Document_layout_parsing'
    name: 'Document-layout-parsing'
    id: 'ev-703d62295cf7cc42'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'node_edge_container'
    name: '--node--edge--container-'
    id: 'ev-9df26abbbe9810f5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_150'
    name: 'resource-150'
    id: 'ev-1b819653cc02bd8d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_151'
    name: 'resource-151'
    id: 'ev-698af446e2a23798'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'UI_to_code_sketch_to_code'
    name: 'UI-to-code--sketch-to-code'
    id: 'ev-371cf735f0d1f61e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'iterative_refinement'
    name: '--iterative-refinement--'
    id: 'ev-97b1b091a45d0217'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_154'
    name: 'resource-154'
    id: 'ev-41d94442143ba22d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_155'
    name: 'resource-155'
    id: 'ev-4e5992288f0e3eea'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Chart_figure_parsing'
    name: 'Chart--figure-parsing'
    id: 'ev-b550797d7c7cf799'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_157'
    name: '-----'
    id: 'ev-ac2318b2abe1b00d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_158'
    name: 'resource-158'
    id: 'ev-4b18a3b9b998f0b4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_159'
    name: 'resource-159'
    id: 'ev-d2e6ab25a61293a8'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Self_ensemble'
    name: 'Self-ensemble'
    id: 'ev-1c4e34d514130a57'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_161'
    name: '-----'
    id: 'ev-8eba7995217fb96a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_162'
    name: 'resource-162'
    id: 'ev-f7851b62d4ae6c53'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'single_shot_image_captioning_multi_pass_structured_extraction'
    name: '--single-shot-image-captioning-----multi-pass-structured-extract'
    id: 'ev-bf76964022cd66bc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-1c034013035715b1'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_06_17'
    name: '06---17'
    id: 'ev-dda37f5c73f0af5f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_166'
    name: 'resource-166'
    id: 'ev-c45f2e34161fa672'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_167'
    name: 'resource-167'
    id: 'ev-e0ebb65742e48994'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_07_EXTRACTOR_LAYER'
    name: '07--EXTRACTOR-LAYER'
    id: 'ev-46b46541ef2e9977'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Multi_Extractor_Layer'
    name: 'Multi-Extractor-Layer'
    id: 'ev-d6d011983620eae9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'extractor_Element_Registry'
    name: '-extractor----Element-Registry-'
    id: 'ev-431585bdf6a0f5b6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_171'
    name: 'resource-171'
    id: 'ev-f407750e4d4ee510'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'draw_io_XML_Parser'
    name: 'drawio-XML-Parser'
    id: 'ev-4872fd13e296de91'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_173'
    name: 'resource-173'
    id: 'ev-247988984a3314a2'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'PowerPoint_Shape_Parser'
    name: 'PowerPoint-Shape-Parser'
    id: 'ev-4879959b8399fcc7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_175'
    name: 'resource-175'
    id: 'ev-974586519e951bb7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'PDF_Vector_Text_Parser'
    name: 'PDF-Vector--Text-Parser'
    id: 'ev-c91e05c7239c6ac3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_177'
    name: 'resource-177'
    id: 'ev-aa917340c71f880d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'OCR_Extractor'
    name: 'OCR-Extractor'
    id: 'ev-7a00f826cb3d7256'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_179'
    name: 'resource-179'
    id: 'ev-8f0f4b6733b437d5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Azure_Icon_Classifier'
    name: 'Azure-Icon-Classifier'
    id: 'ev-f4a3c9b59e4060ac'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_181'
    name: 'resource-181'
    id: 'ev-ca921a4bc0a659cf'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Connector_Arrow_Resolver'
    name: 'Connector--Arrow-Resolver'
    id: 'ev-bf1cbc4cca912816'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_183'
    name: 'resource-183'
    id: 'ev-5c073f623d20f84e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Container_Boundary_Detector'
    name: 'Container--Boundary-Detector'
    id: 'ev-a2880da762b9fc5a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_185'
    name: 'resource-185'
    id: 'ev-a6a31427400a7363'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'VLM_Semantic_Extractor'
    name: 'VLM-Semantic-Extractor'
    id: 'ev-d03452f7f606ddd3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_187'
    name: 'resource-187'
    id: 'ev-27cc418b4ceb9fea'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Element_Registry'
    name: '-Element-Registry--'
    id: 'ev-180d91adebb55720'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-9f0b16cfdac76724'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_07_17'
    name: '07---17'
    id: 'ev-e2d87e095671a35a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_191'
    name: 'resource-191'
    id: 'ev-4ccdd5c4b5b3737f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_192'
    name: 'resource-192'
    id: 'ev-40610dc65e3bf8e7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_08_NORMALIZATION'
    name: '08--NORMALIZATION'
    id: 'ev-2c3d5b3fae18de9b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'ID_Registry'
    name: '--ID--Registry-'
    id: 'ev-5bb8a51ec338dd47'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_195'
    name: 'resource-195'
    id: 'ev-961c76d4c903be67'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_196'
    name: '--'
    id: 'ev-c6d9ffd6b69a286b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'element_json'
    name: 'elementjson'
    id: 'ev-7d6361efec9a0ed3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'elementId'
    name: 'elementId-----'
    id: 'ev-36e35925d9f8997b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'kind_icon_text_connector_container_legend_note'
    name: 'kind----icon--text--connector--container--legend--note'
    id: 'ev-c101bd2aba4ea3fa'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'label'
    name: 'label-----'
    id: 'ev-7301202adc00aa87'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'bbox'
    name: 'bbox-----'
    id: 'ev-47c054601c0bdcb3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'source_evidence'
    name: 'source-evidence-----'
    id: 'ev-111acbbfc51ce69b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'confidence'
    name: 'confidence-----'
    id: 'ev-c471c7c91b7a9412'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'parent_container'
    name: 'parent-container-----'
    id: 'ev-a3eccbfc50197718'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Azure_resource_candidate'
    name: 'Azure-resource-candidate-----'
    id: 'ev-c0d2dcc80aa4e1e2'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'deployability'
    name: 'deployability------'
    id: 'ev-d0d92f35750d0b85'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_207'
    name: 'resource-207'
    id: 'ev-4145331ac1ceef33'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_208'
    name: 'resource-208'
    id: 'ev-82b28385d97f6289'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_209'
    name: '-------'
    id: 'ev-9bd42306917a12cc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_210'
    name: 'resource-210'
    id: 'ev-163592556b938766'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_211'
    name: 'resource-211'
    id: 'ev-0a0953d29a643936'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Single_Source_of_Truth'
    name: 'Single-Source-of-Truth'
    id: 'ev-ff16e87167a68542'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Extractor_Registry'
    name: '-Extractor---Registry-'
    id: 'ev-387181ba174a8bd3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_214'
    name: 'resource-214'
    id: 'ev-61b65cb187714a71'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_215'
    name: 'resource-215'
    id: 'ev-5c8dd007f95f06b0'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_216'
    name: '--'
    id: 'ev-456a213bf779bbdd'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'confidence'
    name: '--confidence----'
    id: 'ev-9665098259274021'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_218'
    name: 'resource-218'
    id: 'ev-a170e021904396ef'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_219'
    name: 'resource-219'
    id: 'ev-19f571220cdd9cf9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_220'
    name: '-'
    id: 'ev-edb12f04880cef96'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Graph_Reconstruction_IaC_Generator'
    name: 'Graph-ReconstructionIaC-Generator---'
    id: 'ev-1398efcb2ecc90a6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-95399f9473793801'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_08_17'
    name: '08---17'
    id: 'ev-48d4bd28d725c85a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_224'
    name: 'resource-224'
    id: 'ev-05b5c858c3d0b17e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_225'
    name: 'resource-225'
    id: 'ev-e7fc89e9b02929f8'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_09_GRAPH'
    name: '09--GRAPH'
    id: 'ev-3b01ed2c70fec871'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Graph'
    name: '-Architecture-Graph-'
    id: 'ev-9c8383ad9b883859'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_228'
    name: 'resource-228'
    id: 'ev-4b70d44e2235fc34'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Shape'
    name: '-Shape'
    id: 'ev-36df4f429cc96d31'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Node'
    name: 'Node'
    id: 'ev-8f5783ea5eabe30d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_231'
    name: 'resource-231'
    id: 'ev-4c4a04841ff0c53f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Arrow'
    name: '-Arrow'
    id: 'ev-98e0e283f1a7dfd9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Edge'
    name: 'Edge'
    id: 'ev-bd9b11db69e33bc6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_234'
    name: 'resource-234'
    id: 'ev-d99023addee30b43'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Boundary'
    name: '--Boundary'
    id: 'ev-252adf72f29e851c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Container'
    name: 'Container'
    id: 'ev-13e6fc7f538e633a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_237'
    name: 'resource-237'
    id: 'ev-123037a38e0505fe'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_238'
    name: '---'
    id: 'ev-24f9a834a2a6c7c9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Semantic_Hint'
    name: 'Semantic-Hint'
    id: 'ev-de30f80af95ac432'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_240'
    name: 'resource-240'
    id: 'ev-f941c11b12b684f2'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_241'
    name: '-'
    id: 'ev-3ac498c28c1f130a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Dependency_Hint'
    name: 'Dependency-Hint'
    id: 'ev-7f1bb22df6519323'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_243'
    name: 'resource-243'
    id: 'ev-4b5b5383ee0ff7cf'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Legend'
    name: 'Legend'
    id: 'ev-dde102cd4860b80f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Flow_Meaning'
    name: 'Flow-Meaning'
    id: 'ev-3d1423ae0aa780ad'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_246'
    name: '--'
    id: 'ev-9d0b75493d173ac7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_247'
    name: 'resource-247'
    id: 'ev-859278d797dd8b9e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'External_User'
    name: 'External-User'
    id: 'ev-e06acf93a87273a7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_249'
    name: 'resource-249'
    id: 'ev-1e4af984ab71abd2'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Conditional_Access'
    name: 'Conditional-Access'
    id: 'ev-1655c34933c2ccb6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_251'
    name: 'resource-251'
    id: 'ev-47e8dbf5a54c1f70'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'AVD_Service'
    name: 'AVD-Service'
    id: 'ev-948ca6ea0657d643'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_253'
    name: 'resource-253'
    id: 'ev-29fc7ca9e431f666'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Host_Pool'
    name: 'Host-Pool'
    id: 'ev-aa849a22fd1d9541'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_255'
    name: 'resource-255'
    id: 'ev-c90e96c65895fdd5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Firewall'
    name: 'Firewall'
    id: 'ev-5b256cbfbe787bb7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_257'
    name: 'resource-257'
    id: 'ev-9d21452221dbda37'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Internal_Servers'
    name: 'Internal-Servers'
    id: 'ev-8654ecc43951369e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-6bc4f1b7fa84e74d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_09_17'
    name: '09---17'
    id: 'ev-a5caa246be1253a3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_261'
    name: 'resource-261'
    id: 'ev-ddfd93ccbe8fa1b2'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_262'
    name: 'resource-262'
    id: 'ev-8696e36af315f8e0'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_10_INTERMEDIATE_REPRESENTATION'
    name: '10--INTERMEDIATE-REPRESENTATION'
    id: 'ev-a8f891aeeddcb8e5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IaC_Architecture_IR'
    name: 'IaC-----Architecture-IR'
    id: 'ev-f3a0c5883a1ffe2b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_265'
    name: 'resource-265'
    id: 'ev-a926e17ff37bd9dd'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'architecture_ir_json'
    name: 'architectureirjson'
    id: 'ev-93740da57a80363a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_267'
    name: 'resource-267'
    id: 'ev-7935c7665163881f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resources'
    name: 'resources'
    id: 'ev-b13d537187a4dc25'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_269'
    name: 'resource-269'
    id: 'ev-5095c8ff0fa03b63'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'relationships'
    name: 'relationships'
    id: 'ev-44140de6a223b2bf'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_271'
    name: 'resource-271'
    id: 'ev-5403d1db16a3b786'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'containers'
    name: 'containers'
    id: 'ev-0837f3898a49ad29'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_273'
    name: 'resource-273'
    id: 'ev-316e623366f3cb4d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'securityControls'
    name: 'securityControls'
    id: 'ev-821460e9de454f2d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_275'
    name: 'resource-275'
    id: 'ev-4a68a44ad186e098'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'existingResources'
    name: 'existingResources'
    id: 'ev-82d85fa612e2fdb6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_277'
    name: 'resource-277'
    id: 'ev-21317434cf9f8abb'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'manualControls'
    name: 'manualControls'
    id: 'ev-5c9af2a83b96bb8c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_279'
    name: 'resource-279'
    id: 'ev-1010af463c2622be'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'questions'
    name: 'questions'
    id: 'ev-0a6e65bd1aba5a2e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_281'
    name: 'resource-281'
    id: 'ev-75441227f512107d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'warnings'
    name: 'warnings'
    id: 'ev-e0e982e9391554f9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_283'
    name: 'resource-283'
    id: 'ev-a41fefee4d17f142'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'confidence_score'
    name: 'confidence-score'
    id: 'ev-8b2a191ef49951e2'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_285'
    name: 'resource-285'
    id: 'ev-56b606a1aff06f93'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_286'
    name: 'resource-286'
    id: 'ev-eb721934a01f4f4f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Bicep'
    name: 'Bicep'
    id: 'ev-7e86359723801c12'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Azure_IaC'
    name: 'Azure--IaC'
    id: 'ev-568c69eb3b9dabfa'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_289'
    name: 'resource-289'
    id: 'ev-18d6cf0cee695aac'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_290'
    name: 'resource-290'
    id: 'ev-eddfa49f2eafa1e7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Terraform'
    name: 'Terraform'
    id: 'ev-3097478da374711f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IaC'
    name: '--IaC'
    id: 'ev-0ca0b9b299dc3a46'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IR'
    name: '-IR-----'
    id: 'ev-a6bac2b3c0d128c9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-f6dc889ccb842fab'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_10_17'
    name: '10---17'
    id: 'ev-bbacb9184d97c247'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_296'
    name: 'resource-296'
    id: 'ev-aeef17111ec48cfc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_297'
    name: 'resource-297'
    id: 'ev-4414de8893aa0407'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_11_QUESTION_MODEL'
    name: '11--QUESTION-MODEL'
    id: 'ev-b6664bb98a937fb9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_299'
    name: '------'
    id: 'ev-5c6b937e7943877b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_300'
    name: 'resource-300'
    id: 'ev-e740803842048139'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_301'
    name: 'resource-301'
    id: 'ev-1542ddda74ab4ef8'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Blocker'
    name: 'Blocker'
    id: 'ev-8f4945a687a94ed5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_303'
    name: '---'
    id: 'ev-3407d9f53682c433'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_304'
    name: 'resource-304'
    id: 'ev-b445bdbe39915fdb'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_305'
    name: 'resource-305'
    id: 'ev-11a2317ebed4dbe3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Risk'
    name: 'Risk'
    id: 'ev-dda565101ad953a3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_307'
    name: '---'
    id: 'ev-068beb5249fce997'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_308'
    name: 'resource-308'
    id: 'ev-ec3a724eb22c4314'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_309'
    name: 'resource-309'
    id: 'ev-16dfa1da6cd0e0a1'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Optional'
    name: 'Optional'
    id: 'ev-1088103f947f508e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_311'
    name: '-'
    id: 'ev-76dd92bf8b431a6d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_312'
    name: 'resource-312'
    id: 'ev-6fda81fe734ba163'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_313'
    name: 'resource-313'
    id: 'ev-4dda241e318f32de'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Manual_Control'
    name: 'Manual-Control'
    id: 'ev-92d28b098e83c509'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Graph_API'
    name: 'Graph--API----'
    id: 'ev-0a04aef0efe13738'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_316'
    name: '-'
    id: 'ev-e1bf92b85bc6d306'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_317'
    name: 'resource-317'
    id: 'ev-88f5d8163eaa63a4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Korea_Central'
    name: '--Korea-Central-'
    id: 'ev-233346ddf0b93565'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_319'
    name: 'resource-319'
    id: 'ev-ab3c5f4d972ad01e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'VNet_CIDR'
    name: 'VNet-CIDR-'
    id: 'ev-02f7cc2452366653'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_321'
    name: 'resource-321'
    id: 'ev-d8b0771f1a144fc5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Azure_Firewall_SKU_Standard'
    name: 'Azure-Firewall-SKU-Standard-'
    id: 'ev-a36932e485a854b0'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_323'
    name: 'resource-323'
    id: 'ev-0e0cc2842fcf8da8'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Conditional_Access'
    name: 'Conditional-Access--'
    id: 'ev-be7470c641e7f470'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-08d4117f9b69ee1a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_11_17'
    name: '11---17'
    id: 'ev-289b90b84ce7b52c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_327'
    name: 'resource-327'
    id: 'ev-22f9e8c75c6d552f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_328'
    name: 'resource-328'
    id: 'ev-df138c2af0c0e84e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_12_CODE_GENERATION'
    name: '12--CODE-GENERATION'
    id: 'ev-92ecfa6e2a3965a7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IR_Bicep_Terraform'
    name: 'IR--Bicep--Terraform--'
    id: 'ev-2e7ad886e871206c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_331'
    name: 'resource-331'
    id: 'ev-8fbf6b636a815cc5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_IR'
    name: 'Architecture--IR'
    id: 'ev-37a9f0216c77fa60'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_333'
    name: 'resource-333'
    id: 'ev-0a3e682ed98b2052'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_334'
    name: 'resource-334'
    id: 'ev-c8e817f3f3d789d5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IR_Bicep_emitter'
    name: 'IR--Bicep-emitter'
    id: 'ev-df94997259438d79'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Raw_Bicep_AVM_Azure'
    name: 'Raw-Bicep---AVM-----Azure---'
    id: 'ev-eacb18d3c19d095c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_337'
    name: 'resource-337'
    id: 'ev-b432cefca50a9e2c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_338'
    name: 'resource-338'
    id: 'ev-8cb0a940b44260b1'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IR_Terraform_emitter'
    name: 'IR--Terraform-emitter'
    id: 'ev-9dc00639269eca70'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_2'
    name: '2-------'
    id: 'ev-1d1ea179d543a1d7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_341'
    name: 'resource-341'
    id: 'ev-73ee3510bf454e53'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_342'
    name: 'resource-342'
    id: 'ev-12683d54d7415384'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Bicep_Terraform'
    name: 'Bicep--Terraform---'
    id: 'ev-686f06ceb212acc3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-ae018bd16b7241c8'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_12_17'
    name: '12---17'
    id: 'ev-bd3dafaccf50abf4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_346'
    name: 'resource-346'
    id: 'ev-e617d6369980d229'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_347'
    name: 'resource-347'
    id: 'ev-95a14dca55285a2d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_13_DESIGN_SPECIFICATION'
    name: '13--DESIGN-SPECIFICATION'
    id: 'ev-2f3f9a50355c7503'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_349'
    name: '------'
    id: 'ev-c8edcdb35b3e9d21'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IaC_Report'
    name: 'IaC---------Report---'
    id: 'ev-9ae06cf81e0f4b86'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_351'
    name: 'resource-351'
    id: 'ev-2f54d5b6a55d9b62'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_352'
    name: '--'
    id: 'ev-db09fc58b82d62c8'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'architecture_spec_md_Table_of_Contents'
    name: 'architecture-specmd----Table-of-Contents'
    id: 'ev-bd2b32fe87eb5e84'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_01'
    name: '01-----'
    id: 'ev-1a7a219b105256a6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_02_SKU'
    name: '02-----SKU----'
    id: 'ev-c1e298a136f35b2d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_03_VNet'
    name: '03------VNet--'
    id: 'ev-5c83f17b30b955a1'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_04'
    name: '04-----'
    id: 'ev-6284b9015ce97eed'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_05_PIM'
    name: '05-------PIM'
    id: 'ev-dbf61e79ea7a24bc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_06'
    name: '06------'
    id: 'ev-a216907fd51e4b7a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_360'
    name: 'resource-360'
    id: 'ev-ff014b0f67030b83'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'A'
    name: 'A'
    id: 'ev-a3cc9e195dfba081'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_IR'
    name: 'Architecture-IR---'
    id: 'ev-0f7e3faba6ac4fce'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resources_relationships_securityControls_questions'
    name: 'resources--relationships--securityControls--questions---'
    id: 'ev-041662fe1c4b5519'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_364'
    name: 'resource-364'
    id: 'ev-3d6230b3998618b1'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'B'
    name: 'B'
    id: 'ev-b179ad0bacfb3341'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Traceability'
    name: '--Traceability'
    id: 'ev-ae73c20fc5c85a32'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'evidence_IaC'
    name: '----evidence--IaC----'
    id: 'ev-a4f5a7d77c3d2cb9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_368'
    name: 'resource-368'
    id: 'ev-41682b47c6d2ffcb'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'C'
    name: 'C'
    id: 'ev-b01af9b58dc6f990'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Report'
    name: '-Report--'
    id: 'ev-ef235c7f4643730e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Markdown_Word_docx_PDF'
    name: 'Markdown--Worddocx--PDF-------'
    id: 'ev-b6a5b951f6ff2e24'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_372'
    name: 'resource-372'
    id: 'ev-c2d6bbaaf99028e0'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'architecture_spec_md'
    name: 'architecture-specmd'
    id: 'ev-fcd89a6d6476c37b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_374'
    name: 'resource-374'
    id: 'ev-fa4f250920ebcdbc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'architecture_spec_docx'
    name: 'architecture-specdocx'
    id: 'ev-a988077c986ba2e4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_376'
    name: 'resource-376'
    id: 'ev-23b927c6443b3c2d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'architecture_spec_pdf'
    name: 'architecture-specpdf'
    id: 'ev-701c36826192c86f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-647b7a554d9ac774'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_13_17'
    name: '13--17'
    id: 'ev-19b4aa311b556f61'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_380'
    name: 'resource-380'
    id: 'ev-d45bae588b5111e1'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_381'
    name: 'resource-381'
    id: 'ev-d9865094ccebfe8b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_14_VALIDATION'
    name: '14--VALIDATION'
    id: 'ev-7e53667c42cd8583'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_383'
    name: '----'
    id: 'ev-1f3a7ed734e1c572'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_384'
    name: 'resource-384'
    id: 'ev-f6c803ee836e3434'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Bicep'
    name: 'Bicep-'
    id: 'ev-28df8267b486880b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_386'
    name: 'resource-386'
    id: 'ev-48494b443c612fcc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'bicep_format'
    name: 'bicep-format'
    id: 'ev-b1d25e8f9922d710'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_388'
    name: 'resource-388'
    id: 'ev-1cd42bee55665d49'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'bicep_lint'
    name: 'bicep-lint'
    id: 'ev-be5664a1e4ab8a34'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_390'
    name: 'resource-390'
    id: 'ev-2b5cd3638bd2e752'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'bicep_build'
    name: 'bicep-build'
    id: 'ev-8fc4a1ffcee7e24e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_392'
    name: 'resource-392'
    id: 'ev-c28fc1eb24501787'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'az_deployment_validate'
    name: 'az-deployment-validate'
    id: 'ev-949fc8d3aa6d8702'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_394'
    name: 'resource-394'
    id: 'ev-78f97b6ee4e74606'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'az_deployment_what_if'
    name: 'az-deployment-what-if'
    id: 'ev-a8ec92c41556d6a9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_396'
    name: 'resource-396'
    id: 'ev-f19615710342d55f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Terraform'
    name: 'Terraform-'
    id: 'ev-4aa2919b6d82f922'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_398'
    name: 'resource-398'
    id: 'ev-9b2d73c680115bda'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'terraform_fmt'
    name: 'terraform-fmt'
    id: 'ev-bac1e199ccc4398f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_400'
    name: 'resource-400'
    id: 'ev-831083dc598abf97'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'terraform_validate'
    name: 'terraform-validate'
    id: 'ev-b75a4eb42622293b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_402'
    name: 'resource-402'
    id: 'ev-393d9946c9071a5d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'tflint'
    name: 'tflint'
    id: 'ev-656e0263d41e5755'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_404'
    name: 'resource-404'
    id: 'ev-65fc4a7a3e39c8d7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'terraform_plan'
    name: 'terraform-plan'
    id: 'ev-9b82d0aa671bb665'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_406'
    name: 'resource-406'
    id: 'ev-ac342770b71bc6c6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'validation_report_md'
    name: 'validation-reportmd'
    id: 'ev-f04e23744c15bfa5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_408'
    name: 'resource-408'
    id: 'ev-a707e15adbf29024'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'unresolved_questions_md'
    name: 'unresolved-questionsmd'
    id: 'ev-ca73c9998b44abad'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_410'
    name: 'resource-410'
    id: 'ev-87e39a77084a8c6e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'deployment_plan_md'
    name: 'deployment-planmd'
    id: 'ev-8ce585c0a1ee573d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-979c16893892ac64'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_14_17'
    name: '14----17'
    id: 'ev-a4ecb25a5c84b472'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_414'
    name: 'resource-414'
    id: 'ev-20c29c1ebffe4e28'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_415'
    name: 'resource-415'
    id: 'ev-e987cabf54eb4432'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_15_MVP_SCOPE'
    name: '15--MVP-SCOPE'
    id: 'ev-327279756ed135a8'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_1_MVP'
    name: '-1-MVP'
    id: 'ev-f383eb5a70c19f0f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_418'
    name: 'resource-418'
    id: 'ev-55a6c94676173997'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_419'
    name: 'resource-419'
    id: 'ev-7c8c9e49443a2940'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_420'
    name: 'resource-420'
    id: 'ev-3c6456a88cffdd97'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_421'
    name: 'resource-421'
    id: 'ev-fa085a6443b36d7f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_422'
    name: 'resource-422'
    id: 'ev-44c92082857bcded'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'draw_io_XML'
    name: 'drawio-XML'
    id: 'ev-3ae46715a0318334'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_424'
    name: 'resource-424'
    id: 'ev-1184020f8a7ce16e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'PowerPoint_PPTX'
    name: 'PowerPoint-PPTX'
    id: 'ev-754816c008d169e9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_426'
    name: 'resource-426'
    id: 'ev-fc799d622b2a7271'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'PNG'
    name: 'PNG-'
    id: 'ev-603454d62d891b8a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_428'
    name: 'resource-428'
    id: 'ev-ac2b2588d9ee104c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_429'
    name: 'resource-429'
    id: 'ev-46b04dce6ef35021'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_430'
    name: 'resource-430'
    id: 'ev-79216ef7b6c7e7e6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_431'
    name: '-'
    id: 'ev-05393605497f67e6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_432'
    name: 'resource-432'
    id: 'ev-acc84da6c28be7af'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Resource_Group'
    name: 'Resource-Group'
    id: 'ev-02fdb31d47505068'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_434'
    name: 'resource-434'
    id: 'ev-8d2ad686ef5e5c68'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'VNet_Subnet_NSG_Route_Table'
    name: 'VNet--Subnet--NSG--Route-Table'
    id: 'ev-157969f9c79ce1e4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_436'
    name: 'resource-436'
    id: 'ev-43f54671747ce5e5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Azure_Firewall'
    name: 'Azure-Firewall'
    id: 'ev-a8bb94e2f1ff0da5'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_438'
    name: 'resource-438'
    id: 'ev-cd8a4a90473103f6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'AVD_Workspace_Host_Pool_App_Group'
    name: 'AVD-Workspace--Host-Pool--App-Group'
    id: 'ev-99ebe722c1ed7ff9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_440'
    name: 'resource-440'
    id: 'ev-b83bbe9dcb78d62b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Log_Analytics_Diagnostic_Settings'
    name: 'Log-Analytics--Diagnostic-Settings'
    id: 'ev-872c8b50ea71db02'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_442'
    name: 'resource-442'
    id: 'ev-1887b65a8b3aaa73'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_443'
    name: 'resource-443'
    id: 'ev-8f9913ab4c217cfc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_444'
    name: 'resource-444'
    id: 'ev-6b50345f7432fa32'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_445'
    name: 'resource-445'
    id: 'ev-2aff140c18c3ac5b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_446'
    name: 'resource-446'
    id: 'ev-4729608b619a01fe'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'architecture_ir_json'
    name: 'architectureirjson'
    id: 'ev-80f090052a105705'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_448'
    name: 'resource-448'
    id: 'ev-f40b3ae4217c3cfe'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'detected_elements_csv'
    name: 'detected-elementscsv'
    id: 'ev-baab45d89a312a81'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_450'
    name: 'resource-450'
    id: 'ev-8f773f582f022541'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'iac_readiness_report_md'
    name: 'iac-readiness-reportmd'
    id: 'ev-9a8ab69f9426cdbd'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_452'
    name: 'resource-452'
    id: 'ev-b0a5cbf715307f6c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'main_bicep'
    name: 'mainbicep'
    id: 'ev-cd3754d63177df63'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_454'
    name: 'resource-454'
    id: 'ev-ecc9be87130a6e5b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'validation_report_md'
    name: 'validation-reportmd'
    id: 'ev-4a632d5f73a5efc8'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-4de259c0d7525cb9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_15_17'
    name: '15----17'
    id: 'ev-2e239726ef4c9b9f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_458'
    name: 'resource-458'
    id: 'ev-96c3816e056a2808'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_459'
    name: 'resource-459'
    id: 'ev-a77aa4a3e3db7d52'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_16_ROADMAP'
    name: '16--ROADMAP'
    id: 'ev-7b299ee5b8769a86'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_461'
    name: '--'
    id: 'ev-b72eee3125d23ba6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_462'
    name: 'resource-462'
    id: 'ev-878ffc0e5b8de0a6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_1'
    name: '1'
    id: 'ev-c454084edba05fdb'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_464'
    name: 'resource-464'
    id: 'ev-4e255646f33994ba'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Phase_1'
    name: 'Phase-1'
    id: 'ev-b01a59642b45ff2d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Diagram_Understanding_Engine'
    name: 'Diagram-Understanding-Engine'
    id: 'ev-e983da3783d5b913'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_467'
    name: 'resource-467'
    id: 'ev-ea42ffcaaabfa6b2'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_2'
    name: '2'
    id: 'ev-75063b4af078270f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_469'
    name: 'resource-469'
    id: 'ev-eaa3144a4e3152bb'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Phase_2'
    name: 'Phase-2'
    id: 'ev-4952abc4b205dfc0'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_IR_Compiler'
    name: 'Architecture-IR-Compiler'
    id: 'ev-2ac9addb6ff06f8f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_472'
    name: 'resource-472'
    id: 'ev-195b4b0815e9155d'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_3'
    name: '3'
    id: 'ev-c8b116c895f459a6'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_474'
    name: 'resource-474'
    id: 'ev-4f507e855cbbf92b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Phase_3'
    name: 'Phase-3'
    id: 'ev-b0613666adf2a906'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Bicep_Generator'
    name: 'Bicep-Generator'
    id: 'ev-41d7f059e1a75144'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_477'
    name: 'resource-477'
    id: 'ev-2d4208019a76dc43'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_4'
    name: '4'
    id: 'ev-a0fbc24de90b45fd'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_479'
    name: 'resource-479'
    id: 'ev-bad2dd9fc773edae'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Phase_4'
    name: 'Phase-4'
    id: 'ev-f6649a9e6be1efcb'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Validation_What_if'
    name: 'Validation--What-if'
    id: 'ev-dda2e00fdc953ab3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_482'
    name: 'resource-482'
    id: 'ev-44cf3c7974550f7c'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_5'
    name: '5'
    id: 'ev-edccc52ad07c11df'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_484'
    name: 'resource-484'
    id: 'ev-0b5e815d641c9bcc'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Phase_5'
    name: 'Phase-5'
    id: 'ev-514696209c5b20af'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Terraform_Generator'
    name: 'Terraform-Generator'
    id: 'ev-fbe0c871caaaba03'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_487'
    name: 'resource-487'
    id: 'ev-06e68bad2a5a407b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_6'
    name: '6'
    id: 'ev-9bbfbddbf39f4ebd'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_489'
    name: 'resource-489'
    id: 'ev-32a6a151a895e629'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Phase_6'
    name: 'Phase-6'
    id: 'ev-90c32e05753fc69e'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Graph_Policy_Intune_PIM'
    name: 'Graph--Policy--Intune--PIM--'
    id: 'ev-436c1d0415442687'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_492'
    name: 'resource-492'
    id: 'ev-1587c7da9d379328'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_7'
    name: '7'
    id: 'ev-8eadd238b73c8eef'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_494'
    name: 'resource-494'
    id: 'ev-d801152ed0069759'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Phase_7'
    name: 'Phase-7'
    id: 'ev-05deff7ed6b11209'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'GitHub_Actions_Azure_DevOps_PR'
    name: 'GitHub-Actions--Azure-DevOps-PR-'
    id: 'ev-0fb007f65c197bc3'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-e294ebd5380339c9'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'r_16_17'
    name: '16---17'
    id: 'ev-5f533def541eed55'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_499'
    name: 'resource-499'
    id: 'ev-937c678a5bd004a4'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'VISION'
    name: 'VISION'
    id: 'ev-922be4409aa28630'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_501'
    name: '----------'
    id: 'ev-c381e059f50fca88'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_502'
    name: 'resource-502'
    id: 'ev-6158e67a8a72f337'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_Understanding_Engine'
    name: 'Architecture-Diagram--Understanding-Engine'
    id: 'ev-794cd818b007ac5f'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_504'
    name: 'resource-504'
    id: 'ev-45ca70e28afbc673'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_IR_Compiler'
    name: 'Architecture-IR--Compiler'
    id: 'ev-472e9cc0cb0a0977'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_506'
    name: 'resource-506'
    id: 'ev-9d5d1161466e3a8a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'IaC_Generator'
    name: 'IaC--Generator'
    id: 'ev-43615029073ebf9a'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'resource_508'
    name: 'resource-508'
    id: 'ev-487ca8cc3dc21c5b'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Validation_Automation'
    name: 'Validation--Automation'
    id: 'ev-a9a95e62cb7c4a93'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_Understanding_Engine_Architecture_IR_Compil'
    name: 'Architecture-Diagram-Understanding-Engine--Architecture-IR-Compi'
    id: 'ev-f7727c2a16f438c7'
    category: 'unknown'
    provider: 'neutral'
  }
  {
    symbolicName: 'Architecture_Diagram_to_IaC_Compiler'
    name: 'Architecture-Diagram-to-IaC-Compiler'
    id: 'ev-7777b2abf870ece2'
    category: 'unknown'
    provider: 'neutral'
  }
]

@description('Draft architecture relationships extracted from source diagrams.')
var inferredRelationships = [
  {
    id: 'ev-f294fc68ec30c8a6'
    from: 'ev-e7bbd27415313083'
    to: 'ev-f37f516dcc2283f7'
    kind: 'dependency'
  }
  {
    id: 'ev-6907beb8ef5e2047'
    from: 'ev-d75715e51f99c0a2'
    to: 'ev-bfd5f1f4d71ab858'
    kind: 'dependency'
  }
  {
    id: 'ev-8dcb1b0897f09e14'
    from: 'ev-de7160a40eb9223f'
    to: 'ev-5fc729aa7775f648'
    kind: 'dependency'
  }
  {
    id: 'ev-77c3cc49a7491253'
    from: 'ev-1dc24dbc285f24c0'
    to: 'ev-9b9c59e7d5f40a9c'
    kind: 'dependency'
  }
  {
    id: 'ev-3db259741211d84f'
    from: 'ev-43d26d357ccb054b'
    to: 'ev-22f7448237e4d4c8'
    kind: 'dependency'
  }
  {
    id: 'ev-959b0ba5386a4a38'
    from: 'ev-22f7448237e4d4c8'
    to: 'ev-89d21ce030230074'
    kind: 'dependency'
  }
  {
    id: 'ev-8c6ff4142e381624'
    from: 'ev-5149950fac6a6cbe'
    to: 'ev-a9789bf0b61362cc'
    kind: 'dependency'
  }
  {
    id: 'ev-b36e6b94371dde32'
    from: 'ev-97dd4242e290ade5'
    to: 'ev-b601b4a18aff5358'
    kind: 'dependency'
  }
  {
    id: 'ev-0dc9d5f8e42a0c50'
    from: 'ev-ae0b0374064523e0'
    to: 'ev-38fbb44d8b75b83c'
    kind: 'dependency'
  }
  {
    id: 'ev-d3f2336541638193'
    from: 'ev-38fbb44d8b75b83c'
    to: 'ev-7cbc88cd96c6a8ed'
    kind: 'dependency'
  }
  {
    id: 'ev-479fc7cd3ac042eb'
    from: 'ev-38fbb44d8b75b83c'
    to: 'ev-7cbc88cd96c6a8ed'
    kind: 'dependency'
  }
  {
    id: 'ev-af400eeedec84811'
    from: 'ev-38fbb44d8b75b83c'
    to: 'ev-7cbc88cd96c6a8ed'
    kind: 'dependency'
  }
  {
    id: 'ev-a740bc3b6ba68e82'
    from: 'ev-4b70d44e2235fc34'
    to: 'ev-8f5783ea5eabe30d'
    kind: 'dependency'
  }
  {
    id: 'ev-24ecb66426564988'
    from: 'ev-4c4a04841ff0c53f'
    to: 'ev-bd9b11db69e33bc6'
    kind: 'dependency'
  }
  {
    id: 'ev-f40f4abbe413efe7'
    from: 'ev-d99023addee30b43'
    to: 'ev-05b5c858c3d0b17e'
    kind: 'dependency'
  }
  {
    id: 'ev-1da45ba0d9af2176'
    from: 'ev-123037a38e0505fe'
    to: 'ev-de30f80af95ac432'
    kind: 'dependency'
  }
  {
    id: 'ev-867f0dccc910a4c8'
    from: 'ev-f941c11b12b684f2'
    to: 'ev-7f1bb22df6519323'
    kind: 'dependency'
  }
  {
    id: 'ev-1a874d0e8072d169'
    from: 'ev-4b5b5383ee0ff7cf'
    to: 'ev-3d1423ae0aa780ad'
    kind: 'dependency'
  }
  {
    id: 'ev-c3867fe44d1aeabc'
    from: 'ev-859278d797dd8b9e'
    to: 'ev-e7fc89e9b02929f8'
    kind: 'dependency'
  }
  {
    id: 'ev-082231873dc88dc7'
    from: 'ev-1e4af984ab71abd2'
    to: 'ev-1655c34933c2ccb6'
    kind: 'dependency'
  }
  {
    id: 'ev-c0727de664f6cf8f'
    from: 'ev-9d0b75493d173ac7'
    to: 'ev-29fc7ca9e431f666'
    kind: 'dependency'
  }
  {
    id: 'ev-8b39a031bbe62368'
    from: 'ev-29fc7ca9e431f666'
    to: 'ev-aa849a22fd1d9541'
    kind: 'dependency'
  }
  {
    id: 'ev-f429a72e8eca1f88'
    from: 'ev-c90e96c65895fdd5'
    to: 'ev-5b256cbfbe787bb7'
    kind: 'dependency'
  }
  {
    id: 'ev-3d0d79f11cd2b7b6'
    from: 'ev-eb721934a01f4f4f'
    to: 'ev-eddfa49f2eafa1e7'
    kind: 'dependency'
  }
  {
    id: 'ev-5bb11a2e11d270ce'
    from: 'ev-eb721934a01f4f4f'
    to: 'ev-eddfa49f2eafa1e7'
    kind: 'dependency'
  }
  {
    id: 'ev-5bad7f7ef6cd3930'
    from: 'ev-8fbf6b636a815cc5'
    to: 'ev-c8e817f3f3d789d5'
    kind: 'dependency'
  }
  {
    id: 'ev-5d4c00419ae49ce1'
    from: 'ev-df138c2af0c0e84e'
    to: 'ev-8cb0a940b44260b1'
    kind: 'dependency'
  }
  {
    id: 'ev-25bd4b4d2a4e1c99'
    from: 'ev-2d4208019a76dc43'
    to: 'ev-a0fbc24de90b45fd'
    kind: 'dependency'
  }
  {
    id: 'ev-da07ce01adb8c289'
    from: 'ev-6158e67a8a72f337'
    to: 'ev-45ca70e28afbc673'
    kind: 'dependency'
  }
  {
    id: 'ev-c17d9f9628a0f18a'
    from: 'ev-45ca70e28afbc673'
    to: 'ev-937c678a5bd004a4'
    kind: 'dependency'
  }
  {
    id: 'ev-fce3fbb1885ef8f9'
    from: 'ev-9d5d1161466e3a8a'
    to: 'ev-487ca8cc3dc21c5b'
    kind: 'dependency'
  }
]

output inferredResourceCount int = length(inferredResources)
output inferredRelationshipCount int = length(inferredRelationships)
