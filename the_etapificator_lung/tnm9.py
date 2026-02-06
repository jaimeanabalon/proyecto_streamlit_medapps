tnm9_definiciones_t_clinico = {
    'cTX':'El tumor primario no puede ser evaluado. Incluye tumores comprobados por la presencia de células malignas en esputo o lavados bronquiales, pero que no son visualizados mediante imágenes o broncoscopía.',
    'cT0':'Sin evidencia de tumor primario',
    'cT1':'Tumor ≤ 3 cm en su dimensión mayor, rodeado por pulmón o pleura visceral, o en un bronquio lobar o más periférico.',
    'cT1mi':'Minimally invasive adenocarcinoma: adenocarcinoma (≤ 3 cm in greatest dimension) with a predominantly lepidic pattern and ≤ 5 mm invasion in greatest dimension',
    'cT1a':'Tumor ≤ 1 cm in greatest dimension OR Tumor of any size whose invasive component is limited to the bronchial wall and may extend proximal to the main bronchus, this is an uncommon superficial, spreading tumor',
    'cT1b':'Tumor > 1 cm but ≤ 2 cm in greatest dimension',
    'cT1c':'Tumor > 2 cm but ≤ 3 cm in greatest dimension',
    'cT2':['Tumor > 3 cm but ≤ 5 cm in greatest dimension', 'Tumor ≤ 4 cm with one or more of the following features:Invades visceral pleura, Invades an adjacent lobe, Involves main bronchus (up to but not including the carina)', 'associated with atelectasis or obstructive pneumonitis, extending to the hilar regions, involving either part of or the entire lung'],
    'cT2a':'Tumor > 3 cm but ≤ 4 cm in greatest dimension OR Tumor ≤ 4 cm in greatest dimension with one or more of the following features:Invades visceral pleura, Invades an adjacent lobe, Involves main bronchus (up to but not including the carina) or associated with atelectasis or obstructive pneumonitis, extending to the hilar regions, involving either part of or the entire lung',
    'cT2b':'Tumor > 4 cm but ≤ 5 cm in greatest dimension with or without any of the following features:Invades visceral pleura, Invades an adjacent lobe, Involves main bronchus (up to but not including the carina) or associated with atelectasis or obstructive pneumonitis, extending to the hilar regions, involving either part of or the entire lung',
    'cT3':'Tumor > 5 cm but ≤ 7 cm in greatest dimension OR Tumor ≤ 7 cm with one or more of the following features:Invades parietal pleura or chest wall, Invades pericardium, phrenic nerve or azygos vein (Although these structures lie within the mediastinum, the degree of mediastinal penetration by the tumor needed to invade these structures is not counted as T4), Invades thoracic nerve roots (i.e., T1, T2) or stellate ganglion, Separate tumor nodule(s) in the same lobe as the primary',
    'cT4':['Tumor > 7 cm in greatest dimension', 'Tumor of any size with one or more of the following features:Invades mediastinum (except structures listed in T3), thymus, trachea, carina, recurrent laryngeal nerve, vagus nerve, esophagus or diaphragm, Invades heart, great vessels (aorta, superior/inferior vena cava, intrapericardial pulmonary arteries/veins), supra-aortic arteries or brachiocephalic veins, Invades subclavian vessels, vertebral body, lamina, spinal canal, cervical nerve roots or brachial plexus (i.e., trunks, divisions, cords or terminal nerves), Separate tumor nodule(s) in a different ipsilateral lobe than that of the primary']
}

t2_invasion = ['pleura visceral','lobulo adyacente','bronquio principal, no carina','atelectasia y/o neumonía postobstructiva','hilio pulmonar']
t3_invasion = ['pleura parietal','pared torácica','pericardio','nervio frenico','vena azigos','raíces nerviosas torácicas','ganglio estrellado']
t4_invasion = ['timo','traquea','carina','nv. laringeo recurrente','nv.vago','esofago','diafragma','corazón','vena cava inferior','vena cava superior','art venas pulmonares intrapericardicas','arterias supraaorticas','venas braquiocefalicas','vasos subclavios','cuerpo vertebral','lamina vertebral','canal medular','raices nerviosas cervicales','plexo braquial']
tnm9_definiciones_n_clinico = {
    'cNX':'Los ganglios linfáticos regionales no pueden ser evaluados',
    'cN0':'No hay metástasis en los ganglios linfáticos regionales',
    'cN1':'Metástasis en ganglios linfáticos peribronquiales e hiliares ipsilaterales, incluyendo la extensión directa del tumor a estos ganglios linfáticos',
    'cN2':'Metástasis en ganglios linfáticos mediastínicos e hiliares ipsilaterales, incluyendo la extensión directa del tumor a estos ganglios linfáticos; los ganglios subcarinales se incluyen en esta categoría',
    'cN3':'Metástasis en ganglios linfáticos contralaterales mediastínicos, hiliares, escalenos o supraclaviculares; incluye la extensión directa del tumor a estos ganglios linfáticos'
}
tnm9_definiciones_m_clinico = {
    'cMX':'La presencia de metástasis a distancia no puede ser evaluada',
    'cM0':'No hay metástasis a distancia',
    'cM1a':['Presencia de nódulos tumorales malignos en el pulmón contralateral; presencia de derrame pleural o pericárdico maligno; presencia de implantes pleurales o pericárdicos malignos'],
    'cM1b':'Presencia de metástasis a distancia única en un solo órgano (incluye metástasis en glándula suprarrenal)',
    'cM1c':'Presencia de metástasis a distancia múltiples en uno o más órganos'
}
import streamlit as st
import pandas as pd