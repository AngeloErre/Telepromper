# Teleprompter per macOS

Un teleprompter semplice e gratuito, realizzato in **Python** con **Tkinter**, per leggere copioni e presentazioni con scorrimento automatico. È pensato per registrazioni video, lezioni, webinar e interventi davanti alla videocamera.

> **Stato del progetto:** versione iniziale. Il programma è uno script Python, non un'app `.app` autonoma.

## Funzionalità

- **Caricamento di file `.txt`** tramite finestra di selezione.
- **Scelta del font** tra quelli installati sul computer.
- **Dimensione del testo** regolabile (16–120).
- **Velocità di scorrimento** regolabile anche durante la lettura (5–150, valore indicativo in pixel/secondo).
- **Cronometro del tempo trascorso**: conta solo durante lo scorrimento e si ferma in pausa.
- **Modalità a schermo intero** con barra dei controlli nascosta.
- **Tema scuro** con testo chiaro per facilitare la lettura.
- **Pausa automatica** quando lo scorrimento raggiunge la fine del testo.

## Requisiti

- macOS con un'installazione funzionante di **Python 3** e **Tkinter**.
- Nessuna libreria Python di terze parti: il programma usa soltanto la libreria standard.

**Nota per macOS:** il Python di sistema (`/usr/bin/python3`) può avere una versione di Tkinter non compatibile con il sistema operativo. In caso di errori relativi alla versione di macOS o all'avvio dell'interfaccia grafica, installare una distribuzione ufficiale di Python per macOS da [python.org](https://www.python.org/downloads/macos/) e utilizzare quella per eseguire lo script. Non modificare o rimuovere il Python di sistema.

## Installazione e avvio

1. Scarica o clona questo repository.
2. Apri **Terminale** nella cartella contenente `teleprompter_mac.py`.
3. Verifica che Python e Tkinter funzionino:

   ```bash
   python3 --version
   python3 -m tkinter
   ```

   Il secondo comando dovrebbe aprire una finestra di prova di Tkinter; chiudila prima di proseguire.

4. Avvia il programma:

   ```bash
   python3 teleprompter_mac.py
   ```

Non è necessario installare Homebrew.

## Come si usa

1. Fai clic su **Apri TXT** e seleziona un copione in formato `.txt`.
2. Imposta **font**, **dimensione** e **velocità**.
3. Premi **Spazio** per avviare lo scorrimento e il cronometro.
4. Premi nuovamente **Spazio** per mettere in pausa; il tempo trascorso resta memorizzato.
5. Premi **X** per tornare all'inizio: lo scorrimento si ferma e il cronometro torna a `00:00`.
6. Premi **F** per entrare o uscire dalla modalità a schermo intero; **Esc** per uscirne.

### Scorciatoie da tastiera

| Tasto | Azione |
| --- | --- |
| `Spazio` | Avvia / mette in pausa |
| `X` | Torna all'inizio, interrompe e azzera il cronometro |
| `F` | Attiva / disattiva lo schermo intero |
| `Esc` | Esce dallo schermo intero |

> **Attenzione:** le scorciatoie sono globali all'interno della finestra del programma. Quando modifichi i controlli, alcuni tasti possono attivare anche i comandi del teleprompter.

## Formato dei testi

Il programma accetta file `.txt` e prova a leggerli in **UTF-8** (anche con BOM); se necessario, tenta la codifica **Windows-1252**. Per risultati migliori, salva il copione in UTF-8, con paragrafi separati da righe vuote.

## Risoluzione dei problemi

**Errore `name 'Path' is not defined` durante l'apertura del TXT**

Verifica che, all'inizio del file `teleprompter_mac.py`, sia presente:

```python
from pathlib import Path
```

**Errore `macOS 15 (1507) or later required, have instead 15 (1506)`**

Questo messaggio può indicare un problema di compatibilità tra Python, Tkinter/Tk e macOS. Controlla quale interprete stai utilizzando:

```bash
which python3
python3 --version
python3 -m tkinter
```

Se stai usando `/usr/bin/python3`, prova con un'installazione Python per macOS scaricata da python.org. Non è necessario installare Homebrew.

**Il programma non apre il file TXT**

Controlla che il file esista, sia leggibile e sia un file di testo; se possibile, risalvalo in UTF-8.

## Struttura del progetto

```text
.
├── teleprompter_mac.py   # Applicazione principale
└── README.md             # Documentazione
```

## Limiti attuali

- Non è disponibile una funzione di testo specchiato.
- Non è disponibile una modalità dedicata al secondo monitor.
- Non viene generato automaticamente un pacchetto `.app`.
- Non sono previsti salvataggio e ripristino delle preferenze.

## Licenza

**Da definire.** Se desideri consentire il riutilizzo del codice, aggiungi al repository un file `LICENSE` con la licenza scelta (ad esempio MIT). La sola pubblicazione su GitHub non equivale a concedere automaticamente una licenza d'uso.
