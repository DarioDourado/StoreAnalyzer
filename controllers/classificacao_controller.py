import os
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc
import numpy as np

class ClassificacaoController:
    """Controlador para operações de classificação com machine learning"""
    
    def executar_classificacao(self, df):
        """Executa os algoritmos de classificação nos dados"""
        # Preparação dos dados
        df['Sexo'] = df['Sexo'].astype('category').cat.codes

        X = df[['Quantidade', 'Preço', 'Idade', 'Categoria', 'Sexo']]
        y = df['Produto'].apply(lambda x: 1 if x == 'Proteína Whey' else 0)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        modelos = {
            'Regressão Logística': LogisticRegression(),
            'k-NN': KNeighborsClassifier(),
            'Random Forest': RandomForestClassifier()
        }

        resultados = {}
        for nome, modelo in modelos.items():
            modelo.fit(X_train, y_train)
            y_pred = modelo.predict(X_test)

            acc = accuracy_score(y_test, y_pred)
            
            # Garantir que zero_division seja tratado para evitar warnings
            prec = precision_score(y_test, y_pred, average='binary', zero_division=1)
            rec = recall_score(y_test, y_pred, average='binary', zero_division=1)
            f1 = f1_score(y_test, y_pred, average='binary', zero_division=1)

            resultados[nome] = {'Acurácia': acc, 'Precisão': prec, 'Revocação': rec, 'F1-Score': f1}

            fpr, tpr, _ = roc_curve(y_test, modelo.predict_proba(X_test)[:, 1])
            roc_auc = auc(fpr, tpr)

            plt.figure(figsize=(10, 6))
            plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('Taxa de Falsos Positivos')
            plt.ylabel('Taxa de Verdadeiros Positivos')
            plt.title(f'Curva ROC - {nome}')
            plt.legend(loc='lower right')
            plt.tight_layout()
            plt.savefig(f'resultados/graficos/roc_{nome.lower().replace(" ", "_")}.png')
            plt.close()

        return resultados
    
    def mostrar_curvas_roc(self, frame):
        """Exibe as curvas ROC geradas"""
        from PIL import Image, ImageTk
        
        frame_imgs = tk.Frame(frame)
        frame_imgs.pack(fill=tk.BOTH, expand=True)
        
        modelos = {
            'Regressão Logística': 'regressão_logística',
            'k-NN': 'k-nn', 
            'Random Forest': 'random_forest'
        }
        
        i = 0
        for nome_exibicao, nome_arquivo in modelos.items():
            img_path = f'resultados/graficos/roc_{nome_arquivo}.png'
            
            if os.path.exists(img_path):
                try:
                    img_frame = tk.LabelFrame(frame_imgs, text=nome_exibicao, padx=5, pady=5)
                    img_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
                    
                    img = Image.open(img_path)
                    img = img.resize((300, 240), Image.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)
                    
                    # Guardar referência para evitar garbage collection
                    img_frame.image = img_tk
                    
                    lbl_img = tk.Label(img_frame, image=img_tk)
                    lbl_img.pack(fill=tk.BOTH, expand=True)
                    i += 1
                except Exception as e:
                    print(f"Erro ao carregar imagem {img_path}: {str(e)}")
            else:
                print(f"Arquivo não encontrado: {img_path}")
                
        frame_imgs.columnconfigure(0, weight=1)
        frame_imgs.columnconfigure(1, weight=1)
        frame_imgs.columnconfigure(2, weight=1)