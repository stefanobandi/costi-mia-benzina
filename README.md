# ⛽ Costi Mia Benzina

Un'app per tracciare i tuoi costi di benzina e stimare le spese per i prossimi 12 mesi.

## Funzionalità

- 📝 **Inserisci i rifornimenti**: Registra il chilometraggio, litri di benzina e prezzo pagato
- 📊 **Statistiche in tempo reale**: Visualizza subito il costo medio al litro, consumo medio e spese totali
- 📈 **Stima 12 mesi**: L'app calcola automaticamente quanto spenderai nei prossimi 12 mesi
- 📱 **Accessibile da qualsiasi dispositivo**: Funziona su PC, tablet e smartphone
- 🌐 **Online senza installazione**: Basta accedere al link

## Come usarla

### Opzione 1: Streamlit Cloud (CONSIGLIATO - Gratuito e senza installazione)

1. Vai su [Streamlit Cloud](https://streamlit.io/cloud)
2. Accedi con il tuo account GitHub
3. Clicca su "New app"
4. Seleziona:
   - Repository: `stefanobandi/costi-mia-benzina`
   - Branch: `main`
   - Main file path: `app.py`
5. Clicca "Deploy"
6. Accedi all'app dal link fornito (funziona su PC, tablet, cellulare)

### Opzione 2: Esecuzione locale (richiede Python)

Se preferisci eseguirla localmente:

```bash
# Installa le dipendenze
pip install -r requirements.txt

# Avvia l'app
streamlit run app.py
```

L'app si aprirà automaticamente nel browser a `http://localhost:8501`

## Come usare l'app

1. **Inserisci un rifornimento**:
   - Chilometraggio attuale della tua macchina
   - Litri di benzina che hai messo
   - Prezzo pagato in euro

2. **Visualizza le statistiche**:
   - Spesa totale
   - Consumo medio (litri/100km)
   - Costo per km

3. **Vedi le stime**:
   - Dopo 2 rifornimenti, l'app calcolerà la stima per i prossimi 12 mesi
   - Puoi vedere il grafico della spesa cumulativa

## Note

- I dati sono salvati nella sessione del browser (ricaricare la pagina = dati persi)
- Se vuoi dati persistenti, puoi usare un database (contattami se ti serve)

---

Creato con ❤️ da Stefano