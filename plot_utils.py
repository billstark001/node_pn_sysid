import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
from typing import Optional, Tuple, Union, Dict
import numpy as np

CM_TO_INCH = 1/2.54
PT_TO_CM = 0.035277778

def create_precise_figure(
    width_cm: float,
    height_cm: float,
    font_size_pt: float = 9,
    scale_factor: float = 1.0,
    font_family: str = 'Times New Roman',
    margin_cm: float = 0.1,
    latex_mode: bool = False,
    figure_config: Optional[Dict] = None
) -> Tuple[plt.Figure, plt.Axes]:
  
    width_cm *= scale_factor
    height_cm *= scale_factor
    font_size_pt *= scale_factor
    margin_cm *= scale_factor
    
    # font
    plt.rcParams['font.family'] = font_family
    if latex_mode:
        plt.rcParams['text.usetex'] = True
        plt.rcParams['text.latex.preamble'] = r'\usepackage{times}'
    else:
        plt.rcParams['mathtext.fontset'] = 'custom'
        plt.rcParams['mathtext.rm'] = font_family
        plt.rcParams['mathtext.it'] = f'{font_family}:italic'
        plt.rcParams['mathtext.bf'] = f'{font_family}:bold'
    
    # font
    
    plt.rcParams.update({
        'font.size': font_size_pt,        
        'axes.labelsize': font_size_pt, 
        'axes.titlesize': font_size_pt,  
        'xtick.labelsize': font_size_pt,
        'ytick.labelsize': font_size_pt,
        'legend.fontsize': font_size_pt  
    })
    
    # fig
    fig, ax = plt.subplots(figsize=(width_cm*CM_TO_INCH, height_cm*CM_TO_INCH))
    
    # layout
    plt.tight_layout(pad=margin_cm*CM_TO_INCH)
    plt.tight_layout()
    
    # misc
    if figure_config:
        for key, value in figure_config.items():
            try:
                plt.rcParams[key] = value
            except KeyError:
                print(f"Warning: Invalid parameter {key}")
    
    return fig, ax

def save_precise_figure(
    fig: plt.Figure,
    filename: str,
    dpi: int = 300,
    formats: Optional[list] = None,
    transparent: bool = False,
    additional_kwargs: Optional[Dict] = None
) -> None:
  
    if formats is None:
        formats = ['pdf', 'png']
        
    save_kwargs = {
        'dpi': dpi,
        'bbox_inches': 'tight',
        'transparent': transparent
    }
    
    if additional_kwargs:
        save_kwargs.update(additional_kwargs)
    
    for fmt in formats:
        fig.savefig(f'{filename}.{fmt}', format=fmt, **save_kwargs)
