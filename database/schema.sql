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
    
    fonte_id INTEGER NOT NULL, 
    quantidade REAL NOT NULL, 
    tco2_eq REAL NOT NULL,
    mes_ref INTEGER NOT NULL, 
    ano_ref INTEGER NOT NULL,
    registrado_em DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (fonte_id) REFERENCES fontes_emissao(id),
        UNIQUE (fonte_id, mes_ref, ano_ref)
);

CREATE TABLE IF NOT EXISTS fatores_emissao(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    tipo_fonte TEXT NOT NULL UNIQUE, 
    fator_conversao REAL NOT NULL,
    unidade TEXT NOT NULL

);

-- Fatores MCTI iniciais
INSERT OR IGNORE INTO fatores_emissao (tipo_fonte, fator_conversao, unidade) VALUES
    ('energia_eletrica', 0.0289,    'tCO2e/MWh'),
    ('diesel',           0.002603,  'tCO2e/L'),
    ('gasolina',         0.002212,  'tCO2e/L'),
    ('etanol',           0.001457,  'tCO2e/L'),
    ('glp',              0.001578,  'tCO2e/kg'),
    ('residuos',         0.5,       'tCO2e/t');

