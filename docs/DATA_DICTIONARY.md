# Dicionário de Dados e Regras ETL

Este documento define o esquema do Data Warehouse e as regras de validação de dados.

## Modelo de Dados (Star Schema)

### Fatos
**Fact_Freight**: Registros transacionais de movimentação de carga.
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| FreightID | PK, INT | Identificador único. |
| DateID | FK, INT | Referência à dimensão de tempo. |
| RouteID | FK, INT | Referência à dimensão de rota. |
| VehicleID | FK, INT | Referência à dimensão de veículo. |
| FreightValue | DECIMAL(10,2) | Valor total do frete. |
| DieselPrice | DECIMAL(10,2) | Preço do diesel no momento do transporte. |
| WeightTon | DECIMAL(10,2) | Peso total transportado (toneladas). |

### Dimensões
**Dim_Date**: Dimensão de calendário.
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| DateID | PK, INT | Identificador único. |
| IsHarvestSeason | BIT | Indicador de período de safra. |

**Dim_Route**: Informações geográficas.
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| RouteID | PK, INT | Identificador único. |
| Origin/Destination | VARCHAR | Cidades de origem e destino. |
| DistanceKM | INT | Distância da rota em km. |

**Dim_Vehicle**: Frota.
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| VehicleID | PK, INT | Identificador único. |
| PlateNumber | VARCHAR | Placa do veículo. |
| Capacity | INT | Capacidade máxima de carga. |

### Tabelas de Suporte
**Log_Errors**: Registro de falhas de validação.
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| RawData | NVARCHAR(MAX) | Dado original em formato JSON. |
| ErrorMessage | VARCHAR | Motivo da rejeição. |

## Regras de Negócio (ETL)

### Validação Logística (Sanity Check)
Registros que violem estas regras devem ser rejeitados e logados em `Log_Errors`:

1.  **Viabilidade de Velocidade:**
    *   Cálculo: `Velocidade Média = Distância / Tempo Decorrido`.
    *   Regra: Rejeitar se Velocidade Média > 90 km/h.
    *   Regra: Rejeitar se Data/Hora Chegada <= Data/Hora Partida.

2.  **Consistência de Custos:**
    *   Regra: Valor do Frete deve ser estritamente positivo (> 0).

### Padrões de Dados
*   **Datas:** Formato ISO 8601 (YYYY-MM-DD).
*   **Numéricos:** Separador decimal ponto (.).
*   **Texto:** Encoding UTF-8.
