CREATE TABLE IF NOT EXISTS empresas (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    
    razao_social TEXT NOT NULL, 
    cnpj TEXT NOT NULL UNIQUE, 
    setor TEXT NOT NULL,
    meta_anual_tco2 REAL DEFAULT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP


);

CREATE TABLE IF NOT EXISTS fontes_emissao (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 

    empresa_id INTEGER NOT NULL, 
    nome TEXT NOT NULL, 
    tipo TEXT NOT NULL, 
    unidade TEXT NOT NULL,
    ativo INTEGER DEFAULT 1,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (empresa_id)
        REFERENCES empresas(id)

); 

CREATE TABLE IF NOT EXISTS historico_consumo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    id_fonte INTEGER NOT NULL, 
    quantidade REAL NOT NULL, 
    tco2_eq REAL NOT NULL,
    mes_ref INTEGER NOT NULL, 
    ano_ref INTEGER NOT NULL,
    registrado_em DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_fonte) REFERENCES fontes_emissao(id),
        UNIQUE (id_fonte, mes_ref, ano_ref)
);

CREATE TABLE IF NOT EXISTS fatores_emissao(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    tipo_fonte TEXT NOT NULL UNIQUE, 
    fator_conversao REAL NOT NULL,
    unidade TEXT NOT NULL

);

-- Fatores MCTI iniciais
INSERT OR IGNORE INTO fatores_emissao (tipo_fonte, fator_conversao, unidade) VALUES
    ('energia_eletrica', 0.0289, 'tCO2/MWh'),
    ('diesel',           2.603,  'kgCO2e/L'),
    ('gasolina',         2.212,  'kgCO2e/L'),
    ('glp',              1.578,  'kgCO2e/kg'),
    ('residuos',         0.5,    'tCO2e/t');



