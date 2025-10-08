"""
Generate static and interactive figures for the affordability website
Uses matplotlib for static figures and plotly for interactive visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from pathlib import Path
import json

# Set matplotlib style to match PSE brand colors
plt.style.use('seaborn-v0_8-darkgrid')

# PSE Brand Colors (matching frontend)
PSE_COLORS = {
    'forest_green': '#275258',
    'forest_green_light': '#3a6b72',
    'forest_green_lighter': '#e8f0f1',
    'orange': '#fb923c',
    'orange_light': '#fed7aa',
    'white': '#ffffff',
    'black': '#252728',
    'gray': '#6b7280',
    'light_blue': '#C4F2EB'
}

# Set default matplotlib parameters
matplotlib.rcParams['font.family'] = 'Source Sans Pro'
matplotlib.rcParams['font.size'] = 12
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['axes.titlesize'] = 16
matplotlib.rcParams['xtick.labelsize'] = 11
matplotlib.rcParams['ytick.labelsize'] = 11
matplotlib.rcParams['legend.fontsize'] = 11
matplotlib.rcParams['figure.titlesize'] = 18

# Output directory
OUTPUT_DIR = Path(__file__).parent / 'assets'
OUTPUT_DIR.mkdir(exist_ok=True)


def save_figure(fig, filename, formats=['svg', 'webp', 'png'], dpi=300):
    """
    Save figure in multiple formats optimized for web
    
    Args:
        fig: matplotlib figure object
        filename: base filename (without extension)
        formats: list of formats to save
        dpi: resolution for raster formats
    """
    for fmt in formats:
        filepath = OUTPUT_DIR / f"{filename}.{fmt}"
        
        if fmt == 'svg':
            # SVG: Best for web, scalable, small file size
            fig.savefig(filepath, format='svg', bbox_inches='tight', 
                       transparent=True, dpi=dpi)
            print(f"✓ Saved {filepath} (SVG - recommended for web)")
            
        elif fmt == 'webp':
            # WebP: Modern format, excellent compression
            fig.savefig(filepath, format='webp', bbox_inches='tight', 
                       dpi=dpi, quality=90)
            print(f"✓ Saved {filepath} (WebP - modern format)")
            
        elif fmt == 'png':
            # PNG: Fallback for older browsers
            fig.savefig(filepath, format='png', bbox_inches='tight', 
                       dpi=dpi, transparent=True)
            print(f"✓ Saved {filepath} (PNG - fallback)")
            
        else:
            fig.savefig(filepath, bbox_inches='tight', dpi=dpi)
            print(f"✓ Saved {filepath}")


def create_energy_costs_figure():
    """
    Figure 1: Total energy costs breakdown
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sample data - replace with your actual data
    categories = ['Electricity', 'Natural Gas', 'Propane', 'Fuel Oil', 'Wood']
    low_income = [45, 25, 8, 5, 2]  # Billions
    all_households = [120, 80, 15, 10, 5]  # Billions
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, all_households, width, label='All Households',
                   color=PSE_COLORS['forest_green'], alpha=0.8)
    bars2 = ax.bar(x + width/2, low_income, width, label='Low-Income (<80% AMI)',
                   color=PSE_COLORS['orange'], alpha=0.8)
    
    ax.set_xlabel('Energy Source', fontweight='bold', color=PSE_COLORS['forest_green'])
    ax.set_ylabel('Annual Cost (Billions $)', fontweight='bold', color=PSE_COLORS['forest_green'])
    ax.set_title('Household Energy Costs by Source (2022)', 
                fontweight='bold', color=PSE_COLORS['forest_green'], pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:.0f}B',
                   ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    save_figure(fig, 'energy_costs')
    plt.close()


def create_budget_impact_figure():
    """
    Figure 2: Energy burden distribution
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sample data - replace with your actual data
    income_brackets = ['<50% AMI', '50-80% AMI', '80-100% AMI', '100-150% AMI', '>150% AMI']
    burden_pct = [12.5, 8.2, 5.5, 3.8, 2.1]  # % of income
    threshold = 6.0  # 6% threshold line
    
    colors = [PSE_COLORS['orange'] if b > threshold else PSE_COLORS['forest_green'] 
              for b in burden_pct]
    
    bars = ax.bar(income_brackets, burden_pct, color=colors, alpha=0.8, 
                  edgecolor=PSE_COLORS['black'], linewidth=1.5)
    
    # Add threshold line
    ax.axhline(y=threshold, color='red', linestyle='--', linewidth=2, 
              label=f'{threshold}% Affordability Threshold', alpha=0.7)
    
    ax.set_xlabel('Income Bracket (% of Area Median Income)', 
                 fontweight='bold', color=PSE_COLORS['forest_green'])
    ax.set_ylabel('Energy Burden (% of Income)', 
                 fontweight='bold', color=PSE_COLORS['forest_green'])
    ax.set_title('Average Energy Burden by Income Level', 
                fontweight='bold', color=PSE_COLORS['forest_green'], pad=20)
    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, value in zip(bars, burden_pct):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{value:.1f}%',
               ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    save_figure(fig, 'budget_impact')
    plt.close()


def create_ghg_emissions_figure():
    """
    Figure 3: Residential greenhouse gas emissions
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Pie chart - Total emissions
    labels = ['Low-Income\nHouseholds', 'Other\nHouseholds']
    sizes = [28, 72]  # Percentages
    colors = [PSE_COLORS['orange'], PSE_COLORS['forest_green']]
    explode = (0.1, 0)
    
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax1.set_title('Share of Residential GHG Emissions', 
                 fontweight='bold', color=PSE_COLORS['forest_green'], pad=20)
    
    # Bar chart - Emissions by source
    sources = ['Natural Gas', 'Electricity', 'Propane', 'Fuel Oil', 'Wood']
    emissions = [380, 220, 45, 35, 20]  # Million tons CO2e
    
    bars = ax2.barh(sources, emissions, color=PSE_COLORS['forest_green'], alpha=0.8,
                    edgecolor=PSE_COLORS['black'], linewidth=1.5)
    
    ax2.set_xlabel('Annual Emissions (Million tons CO2e)', 
                  fontweight='bold', color=PSE_COLORS['forest_green'])
    ax2.set_title('Residential Emissions by Energy Source', 
                 fontweight='bold', color=PSE_COLORS['forest_green'], pad=20)
    ax2.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for bar, value in zip(bars, emissions):
        width = bar.get_width()
        ax2.text(width, bar.get_y() + bar.get_height()/2.,
                f'{value:.0f}M',
                ha='left', va='center', fontweight='bold', 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    save_figure(fig, 'ghg_emissions')
    plt.close()


def create_interactive_plotly_figure():
    """
    Example: Create interactive figure using Plotly
    These can be embedded in the website as HTML or JSON
    """
    try:
        import plotly.graph_objects as go
        import plotly.io as pio
        
        # Sample data
        categories = ['Space Heating', 'Water Heating', 'Cooling', 'Appliances', 'Other']
        
        fig = go.Figure()
        
        # Add traces for different income groups
        fig.add_trace(go.Bar(
            name='Low-Income',
            x=categories,
            y=[850, 320, 180, 420, 230],
            marker_color=PSE_COLORS['orange']
        ))
        
        fig.add_trace(go.Bar(
            name='All Households',
            x=categories,
            y=[720, 280, 220, 380, 200],
            marker_color=PSE_COLORS['forest_green']
        ))
        
        fig.update_layout(
            title='Annual Energy Costs by End Use',
            xaxis_title='End Use',
            yaxis_title='Average Annual Cost ($)',
            barmode='group',
            font=dict(family="Source Sans Pro", size=14),
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified'
        )
        
        # Save as HTML (can be embedded via iframe)
        html_path = OUTPUT_DIR / 'interactive_costs.html'
        pio.write_html(fig, html_path, include_plotlyjs='cdn')
        print(f"✓ Saved {html_path} (Interactive HTML)")
        
        # Save as JSON (for custom integration)
        json_path = OUTPUT_DIR / 'interactive_costs.json'
        fig.write_json(json_path)
        print(f"✓ Saved {json_path} (Plotly JSON)")
        
    except ImportError:
        print("⚠ Plotly not installed. Install with: pip install plotly")


def generate_all_figures():
    """
    Generate all website figures
    """
    print("=" * 60)
    print("Generating figures for Affordability Website")
    print("=" * 60)
    print()
    
    print("1. Creating Energy Costs figure...")
    create_energy_costs_figure()
    print()
    
    print("2. Creating Budget Impact figure...")
    create_budget_impact_figure()
    print()
    
    print("3. Creating GHG Emissions figure...")
    create_ghg_emissions_figure()
    print()
    
    print("4. Creating Interactive Plotly figure...")
    create_interactive_plotly_figure()
    print()
    
    print("=" * 60)
    print("✓ All figures generated successfully!")
    print(f"✓ Output directory: {OUTPUT_DIR}")
    print("=" * 60)
    print()
    print("USAGE IN HTML:")
    print("  <!-- SVG (recommended) -->")
    print("  <img src='assets/energy_costs.svg' alt='Energy Costs'>")
    print()
    print("  <!-- WebP with PNG fallback -->")
    print("  <picture>")
    print("    <source srcset='assets/energy_costs.webp' type='image/webp'>")
    print("    <img src='assets/energy_costs.png' alt='Energy Costs'>")
    print("  </picture>")
    print()
    print("  <!-- Interactive Plotly -->")
    print("  <iframe src='assets/interactive_costs.html' ")
    print("          width='100%' height='600px' frameborder='0'></iframe>")


if __name__ == "__main__":
    generate_all_figures()
