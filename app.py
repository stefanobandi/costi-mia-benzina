import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="Costi Mia Benzina", layout="wide")

# Titolo
st.title("⛽ Costi Mia Benzina")
st.markdown("Traccia i tuoi costi di benzina e stima le spese per i prossimi 12 mesi")

# Inizializza session state
if 'refueling_data' not in st.session_state:
    st.session_state.refueling_data = []

# Layout a colonne
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Nuovo Rifornimento")
    
    # Input campi
    mileage = st.number_input("Chilometraggio attuale (km)", min_value=0, step=100, format="%d")
    liters = st.number_input("Litri di benzina", min_value=0.0, step=0.1, format="%.2f")
    price = st.number_input("Prezzo pagato (€)", min_value=0.0, step=0.01, format="%.2f")
    
    if st.button("Aggiungi Rifornimento", type="primary"):
        if mileage > 0 and liters > 0 and price > 0:
            st.session_state.refueling_data.append({
                'data': datetime.now(),
                'chilometraggio': mileage,
                'litri': liters,
                'prezzo': price,
                'costo_per_litro': round(price / liters, 3) if liters > 0 else 0
            })
            st.success("✅ Rifornimento aggiunto!")
        else:
            st.error("❌ Inserisci valori validi")

with col2:
    st.subheader("📊 Statistiche")
    
    if st.session_state.refueling_data:
        df = pd.DataFrame(st.session_state.refueling_data)
        
        # Calcoli
        total_spent = df['prezzo'].sum()
        total_liters = df['litri'].sum()
        avg_price_per_liter = total_spent / total_liters if total_liters > 0 else 0
        
        # Se abbiamo almeno 2 rifornimenti, calcola km percorsi e consumo
        if len(df) >= 2:
            km_traveled = df['chilometraggio'].iloc[-1] - df['chilometraggio'].iloc[0]
            if km_traveled > 0:
                consumption_per_100km = (total_liters / km_traveled) * 100
                cost_per_km = total_spent / km_traveled
            else:
                consumption_per_100km = 0
                cost_per_km = 0
        else:
            km_traveled = 0
            consumption_per_100km = 0
            cost_per_km = 0
        
        # Mostra metriche
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric("Speso Totale", f"€ {total_spent:.2f}")
        with metric_col2:
            st.metric("Litri Totali", f"{total_liters:.2f} L")
        with metric_col3:
            st.metric("Prezzo Medio/L", f"€ {avg_price_per_liter:.3f}")
        
        # Seconda riga di metriche
        metric_col4, metric_col5, metric_col6 = st.columns(3)
        
        with metric_col4:
            st.metric("Km Percorsi", f"{km_traveled:.0f} km")
        with metric_col5:
            st.metric("Consumo Medio", f"{consumption_per_100km:.2f} L/100km")
        with metric_col6:
            st.metric("Costo per Km", f"€ {cost_per_km:.4f}")

# Sezione stima 12 mesi
st.subheader("📈 Stima per i Prossimi 12 Mesi")

if st.session_state.refueling_data and len(st.session_state.refueling_data) >= 2:
    df = pd.DataFrame(st.session_state.refueling_data)
    
    # Calcoli per la stima
    total_days = (df['data'].iloc[-1] - df['data'].iloc[0]).days
    total_spent = df['prezzo'].sum()
    
    if total_days > 0:
        # Stima spesa giornaliera
        daily_spending = total_spent / total_days
        estimated_12_months = daily_spending * 365
        
        # Stima basata su km
        total_liters = df['litri'].sum()
        km_traveled = df['chilometraggio'].iloc[-1] - df['chilometraggio'].iloc[0]
        
        if km_traveled > 0:
            consumption_per_100km = (total_liters / km_traveled) * 100
            avg_price_per_liter = total_spent / total_liters
            
            # Se sappiamo i km che farà mediamente, facciamo la stima
            monthly_km = km_traveled / (total_days / 30.44)  # giorni medi per mese
            
            # Stima per 12 mesi
            estimated_km_12months = monthly_km * 12
            estimated_liters_12months = (estimated_km_12months / 100) * consumption_per_100km
            estimated_cost_12months = estimated_liters_12months * avg_price_per_liter
        else:
            estimated_cost_12months = estimated_12_months
            estimated_km_12months = 0
            monthly_km = 0
        
        # Mostra stime
        st.info(f"📌 Basandoti sui dati degli ultimi **{total_days} giorni**:")
        
        col_stima1, col_stima2, col_stima3 = st.columns(3)
        
        with col_stima1:
            st.metric("Stima 12 Mesi", f"€ {estimated_cost_12months:.2f}")
        with col_stima2:
            st.metric("Stima Mensile", f"€ {estimated_cost_12months/12:.2f}")
        with col_stima3:
            st.metric("Km Medi/Mese", f"{monthly_km:.0f} km")
        
        # Grafico stima
        months = [f"Mese {i+1}" for i in range(12)]
        cumulative_costs = [(estimated_cost_12months / 12) * (i + 1) for i in range(12)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=cumulative_costs,
            mode='lines+markers',
            name='Spesa Cumulativa',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Proiezione Spese nei Prossimi 12 Mesi",
            xaxis_title="Mese",
            yaxis_title="Spesa Cumulativa (€)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning("⚠️ Inserisci almeno 2 rifornimenti per vedere le stime")

# Tabella dati
st.subheader("📋 Storico Rifornimenti")

if st.session_state.refueling_data:
    df = pd.DataFrame(st.session_state.refueling_data)
    
    # Formatta la tabella
    df_display = df.copy()
    df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y %H:%M')
    df_display['litri'] = df_display['litri'].apply(lambda x: f"{x:.2f}")
    df_display['prezzo'] = df_display['prezzo'].apply(lambda x: f"€ {x:.2f}")
    df_display['costo_per_litro'] = df_display['costo_per_litro'].apply(lambda x: f"€ {x:.3f}")
    df_display = df_display.rename(columns={
        'data': '📅 Data',
        'chilometraggio': '🚗 Km',
        'litri': '⛽ Litri',
        'prezzo': '💰 Prezzo',
        'costo_per_litro': '💵 €/L'
    })
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Pulsante per eliminare ultimo rifornimento
    if st.button("🗑️ Elimina Ultimo Rifornimento"):
        st.session_state.refueling_data.pop()
        st.rerun()
else:
    st.info("Nessun rifornimento registrato ancora")