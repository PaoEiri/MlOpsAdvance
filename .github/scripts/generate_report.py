#!/usr/bin/env python3
import sys
import json
from datetime import datetime
from pathlib import Path


def load_history():
    """Carga el histórico de métricas"""
    history_file = Path(".github/data/metrics_history.json")
    if history_file.exists():
        with open(history_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def generate_report(accuracy, precision, recall, timestamp, output_path):
    """
    Genera el reporte HTML llenando los valores en el template
    """
    # Leer el template
    template_path = (
        Path(__file__).parent.parent / "templates" / "report.html"
    )

    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Cargar histórico
    history = load_history()

    # Crear el script inline que llenará los valores
    metrics_script = f"""
        // Inyectar datos en el HTML
        fillMetrics({accuracy}, {precision}, {recall}, '{timestamp}');
        
        // Cargar histórico
        const metricsHistory = {json.dumps(history)};
        loadHistory(metricsHistory);
    """

    # Insertar el script antes del cierre del body
    html_content = html_content.replace(
        "document.addEventListener('DOMContentLoaded', function() {\n            // Los valores se inyectarán aquí con un script inline\n        });",
        f"document.addEventListener('DOMContentLoaded', function() {{\n            {metrics_script}\n        }});",
    )

    # Crear directorio si no existe
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Escribir el HTML final
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Report generated: {output_path}")
    print(f"✅ Historical records loaded: {len(history)}")


if __name__ == "__main__":
    accuracy = float(sys.argv[1])
    precision = float(sys.argv[2])
    recall = float(sys.argv[3])
    timestamp = (
        sys.argv[4] if len(sys.argv) > 4 else datetime.now().isoformat()
    )
    output_path = sys.argv[5] if len(sys.argv) > 5 else "report/index.html"

    generate_report(accuracy, precision, recall, timestamp, output_path)