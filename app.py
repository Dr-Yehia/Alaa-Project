import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="Enhanced Monorail Sustainability Assessment",
    page_icon="🚝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# العنوان الرئيسي
st.title("🚝 Enhanced Monorail Sustainability Assessment Tool")
st.markdown("**AI-Powered LCA/LCCA Framework | Cairo University**")
st.markdown("---")

# Sidebar للمدخلات
st.sidebar.header("📊 Input Parameters")

# المواد
st.sidebar.subheader("📦 Materials")
concrete = st.sidebar.number_input("Concrete (1000 m³)", value=700.0, min_value=0.0)
steel = st.sidebar.number_input("Steel (1000 tons)", value=100.0, min_value=0.0)
aluminum = st.sidebar.number_input("Aluminum (1000 tons)", value=5.0, min_value=0.0)
wood = st.sidebar.number_input("Wood (1000 m³)", value=2.0, min_value=0.0)
frp = st.sidebar.number_input("FRP (1000 tons)", value=1.0, min_value=0.0)
glass = st.sidebar.number_input("Glass (1000 m²)", value=0.5, min_value=0.0)

# معدلات إعادة التدوير
st.sidebar.subheader("♻️ Recycling Rates (%)")
steel_recycle = st.sidebar.slider("Steel Recycling", 0, 100, 70)
aluminum_recycle = st.sidebar.slider("Aluminum Recycling", 0, 100, 85)

# العوامل البيئية
st.sidebar.subheader("🌍 Environmental")
carbon_intensity = st.sidebar.number_input("Grid Carbon Intensity (kg CO₂/kWh)", value=0.5, min_value=0.0)
renewable_share = st.sidebar.slider("Renewable Energy (%)", 0, 100, 20)
land_use = st.sidebar.number_input("Land Use Efficiency (pass/ha)", value=5000.0, min_value=0.0)
noise_reduction = st.sidebar.number_input("Noise Reduction (dB)", value=10.0, min_value=0.0)

# العوامل التشغيلية
st.sidebar.subheader("⚙️ Operational")
energy_per_pax = st.sidebar.number_input("Energy (kWh/pax-km)", value=0.15, min_value=0.0)
daily_pax_km = st.sidebar.number_input("Daily Pax-km (1000)", value=500.0, min_value=0.0)
time_savings = st.sidebar.number_input("Time Savings (1000h)", value=2.5, min_value=0.0)
availability = st.sidebar.slider("Availability (%)", 0, 100, 98)

# العوامل الاقتصادية
st.sidebar.subheader("💰 Economic")
construction_cost = st.sidebar.number_input("Construction ($M)", value=2500.0, min_value=0.0)
maintenance_cost = st.sidebar.number_input("Maintenance ($M/yr)", value=50.0, min_value=0.0)
jobs_created = st.sidebar.number_input("Jobs Created", value=5000.0, min_value=0.0)
economic_multiplier = st.sidebar.number_input("Economic Multiplier", value=2.5, min_value=1.0)

# زر التشغيل
if st.sidebar.button("🚀 RUN ASSESSMENT", type="primary", use_container_width=True):
    # === حسابات الطاقة المُجسدة ===
    coefficients = {
        'concrete': 3.19,
        'steel': 63.65,
        'aluminum': 411.03,
        'wood': 6.63,
        'frp': 206.84,
        'glass': 39.77
    }
    
    densities = {
        'concrete': 2400,
        'wood': 600
    }
    
    # الطاقة المُجسدة
    ee_concrete = concrete * 1000 * densities['concrete'] * coefficients['concrete']
    ee_steel = steel * 1000 * coefficients['steel']
    ee_aluminum = aluminum * 1000 * coefficients['aluminum']
    ee_wood = wood * 1000 * densities['wood'] * coefficients['wood']
    ee_frp = frp * 1000 * coefficients['frp']
    ee_glass = glass * 1000 * 10 * coefficients['glass']
    
    # خصومات إعادة التدوير
    steel_credit = ee_steel * (steel_recycle / 100) * 0.70
    aluminum_credit = ee_aluminum * (aluminum_recycle / 100) * 0.85
    
    total_ee = ee_concrete + ee_steel + ee_aluminum + ee_wood + ee_frp + ee_glass - steel_credit - aluminum_credit
    
    # === حسابات الكربون ===
    emission_factors = {
        'concrete': 0.265,
        'steel': 4.450,
        'aluminum': 27.659,
        'wood': 1.203,
        'frp': 16.353,
        'glass': 2.044
    }
    
    carbon_concrete = concrete * 1000 * densities['concrete'] * emission_factors['concrete']
    carbon_steel = steel * 1000 * emission_factors['steel']
    carbon_aluminum = aluminum * 1000 * emission_factors['aluminum']
    carbon_wood = wood * 1000 * densities['wood'] * emission_factors['wood']
    carbon_frp = frp * 1000 * emission_factors['frp']
    carbon_glass = glass * 1000 * 10 * emission_factors['glass']
    
    steel_carbon_credit = carbon_steel * (steel_recycle / 100) * 0.65
    aluminum_carbon_credit = carbon_aluminum * (aluminum_recycle / 100) * 0.90
    
    embodied_co2 = (carbon_concrete + carbon_steel + carbon_aluminum + 
                    carbon_wood + carbon_frp + carbon_glass - 
                    steel_carbon_credit - aluminum_carbon_credit) / 1000  # tons
    
    # === الانبعاثات التشغيلية ===
    effective_carbon = carbon_intensity * (1 - renewable_share / 100.0)
    operational_carbon_intensity = energy_per_pax * effective_carbon * 0.800
    annual_co2_operational = operational_carbon_intensity * daily_pax_km * 1000 * 365 / 1000
    
    total_co2 = annual_co2_operational + embodied_co2
    
    # === النتائج ===
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total CO₂ Emissions", f"{total_co2:,.0f} tons", 
                 delta=f"Embodied: {embodied_co2:,.0f}t")
    
    with col2:
        st.metric("Embodied Energy", f"{total_ee/1000:,.0f} GJ",
                 delta=f"Concrete: {(ee_concrete/total_ee*100):.1f}%")
    
    with col3:
        st.metric("Economic Impact", f"${construction_cost+maintenance_cost*30:,.0f}M",
                 delta=f"Jobs: {jobs_created*economic_multiplier:,.0f}")
    
    with col4:
        renewable_impact = (1 - renewable_share/100) * 100
        st.metric("Renewable Integration", f"{renewable_share}%",
                 delta=f"-{renewable_impact:.0f}% emissions")
    
    st.markdown("---")
    
    # رسوم بيانية
    tab1, tab2, tab3 = st.tabs(["📊 Material Breakdown", "🌍 Environmental Impact", "💰 Economic Analysis"])
    
    with tab1:
        # مخطط دائري للمواد
        materials_data = {
            'Concrete': concrete,
            'Steel': steel,
            'Aluminum': aluminum,
            'Wood': wood,
            'FRP': frp,
            'Glass': glass
        }
        
        fig_materials = px.pie(
            values=list(materials_data.values()),
            names=list(materials_data.keys()),
            title="Material Distribution",
            hole=0.4
        )
        st.plotly_chart(fig_materials, use_container_width=True)
    
    with tab2:
        # مخطط الانبعاثات
        emissions_data = pd.DataFrame({
            'Category': ['Operational CO₂', 'Embodied CO₂'],
            'Value': [annual_co2_operational, embodied_co2]
        })
        
        fig_emissions = px.bar(emissions_data, x='Category', y='Value',
                              title="CO₂ Emissions Breakdown",
                              color='Category')
        st.plotly_chart(fig_emissions, use_container_width=True)
    
    with tab3:
        # التحليل الاقتصادي
        years = list(range(0, 31))
        costs = [construction_cost] + [maintenance_cost] * 30
        cumulative = np.cumsum(costs)
        
        fig_economic = go.Figure()
        fig_economic.add_trace(go.Scatter(x=years, y=cumulative,
                                         mode='lines', name='Cumulative Cost'))
        fig_economic.update_layout(title="30-Year Economic Analysis",
                                  xaxis_title="Year",
                                  yaxis_title="Cost (Million USD)")
        st.plotly_chart(fig_economic, use_container_width=True)
    
    # تقرير مفصل
    st.markdown("---")
    st.subheader("📄 Detailed Assessment Report")
    
    report = f"""
### Materials Assessment
- **Concrete**: {concrete:,.0f} thousand m³
- **Steel**: {steel:,.0f} thousand tons (Recycling: {steel_recycle}%)
- **Aluminum**: {aluminum:,.0f} thousand tons (Recycling: {aluminum_recycle}%)

### Environmental Impact
- **Total CO₂**: {total_co2:,.0f} tons
  - Operational: {annual_co2_operational:,.0f} tons/year
  - Embodied: {embodied_co2:,.0f} tons
- **Total Embodied Energy**: {total_ee:,.0f} MJ ({total_ee/1000:,.0f} GJ)
- **Effective Carbon Intensity**: {effective_carbon:.3f} kg CO₂/kWh

### Operational Performance
- **Energy per Passenger-km**: {energy_per_pax:.3f} kWh
- **Daily Passenger-km**: {daily_pax_km:,.0f} thousand
- **System Availability**: {availability}%

### Economic Analysis
- **Construction Cost**: ${construction_cost:,.0f} million
- **30-Year Maintenance**: ${maintenance_cost*30:,.0f} million
- **Total Jobs**: {jobs_created*economic_multiplier:,.0f} (Multiplier: {economic_multiplier}x)

---
**Assessment Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Methodology**: ISO 14040/14044 LCA + Chen et al. (2022) Calibration
    """
    
    st.markdown(report)
    
    # تحميل التقرير
    st.download_button(
        label="📥 Download Full Report",
        data=report,
        file_name=f"monorail_assessment_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown"
    )
