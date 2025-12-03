# Dicionário de Dados e Governança

Este documento define o esquema de dados analíticos, os payloads de telemetria e as regras de governança para as duas fases do projeto.

---

## 1. Modelo Analítico (Serving Layer)

*Aplicável à **Fase 1 (SQL Server Local)** e à **Fase 2 (Camada Gold/Azure SQL)**.*

O modelo segue a arquitetura **Star Schema** para otimização de consultas em ferramentas de BI (Power BI).

### Fatos

**Fact_Freight**: Consolidação transacional de fretes finalizados.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| FreightID | PK, INT | Identificador único do frete. |
| DateID | FK, INT | Chave para dimensão de tempo. |
| RouteID | FK, INT | Chave para dimensão de rota. |
| VehicleID | FK, INT | Chave para dimensão de veículo. |
| FreightValue | DECIMAL(10,2) | Valor total do frete (R$). |
| DieselPrice | DECIMAL(10,2) | Preço do diesel na data (R$/L). |
| WeightTon | DECIMAL(10,2) | Peso transportado (Toneladas). |

### Dimensões

**Dim_Route**: Dados geográficos e de trajeto.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| RouteID | PK, INT | Identificador único. |
| Origin | VARCHAR(100) | Cidade/Estado de origem. |
| Destination | VARCHAR(100) | Cidade/Estado de destino. |
| DistanceKM | INT | Distância rodoviária oficial. |

**Dim_Vehicle**: Frota e características técnicas.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| VehicleID | PK, INT | Identificador único. |
| PlateNumber | VARCHAR(20) | Placa anonimizada ou hash. |
| Capacity | INT | Capacidade máxima (kg). |

---

## 2. Modelo de Telemetria IoT (Expansão Fase 2)

*Aplicável exclusivamente à **Fase 2 (Azure IoT Hub / Camada Bronze)**.*

Definição do payload JSON enviado pelos sensores embarcados (Simulador C++) para a nuvem.

### Payload de Evento (Raw Sensor Data)

Tópico MQTT: `devices/{device_id}/messages/events/`

```json
{
  "device_id": "TRUCK-001",
  "timestamp": "2025-12-04T14:30:00Z",
  "gps": {
    "lat": -16.686891,
    "lng": -49.264794
  },
  "telemetry": {
    "speed_kmh": 85.5,
    "engine_rpm": 2200,
    "fuel_level_pct": 45.0
  },
  "status": "MOVING" // ENUM: MOVING, IDLE, ERROR
}
```

---

## 3. Regras de Qualidade e Governança (Data Quality)

Regras aplicadas durante o processo de ETL (Python na Fase 1) e pipelines Spark (Databricks na Fase 2).

### Quality Gates (Sanity Check)

Registros que violem as regras abaixo devem ser segregados em tabelas de erro (`Log_Errors` ou `Silver_Quarantine`).

1. **Consistência Física (Velocidade):**
    * *Regra:* `(Distância da Rota / Tempo de Viagem) < 100 km/h`.
    * *Ação:* Rejeitar como anomalia de telemetria se violado.

2. **Viabilidade Temporal:**
    * *Regra:* `Data Chegada > Data Partida`.
    * *Ação:* Rejeitar registros com viagem negativa ou nula.

3. **Integridade Financeira:**
    * *Regra:* `FreightValue > 0` e `DieselPrice > 0`.
    * *Ação:* Bloquear ingestão de fretes sem valor monetário.

### Arquitetura de Dados (Fase 2 - Databricks)

Para a expansão em Big Data, os dados fluem através da arquitetura Medalhão:

* **Bronze:** Dados brutos do IoT Hub (JSON original).
* **Silver:** Dados limpos, tipados e validados pelas regras acima (Parquet/Delta).
* **Gold:** Modelo Star Schema agregado para consumo do Power BI (Delta Tables).
