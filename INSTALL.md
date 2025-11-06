# Instrucciones de instalación

## Instalar dependencias

Ejecuta el siguiente comando en tu terminal dentro del entorno virtual:

```bash
pip install -r requirements.txt
```

O instala las nuevas dependencias individualmente:

```bash
pip install reportlab matplotlib
```

## Dependencias añadidas para exportar PDF

- **reportlab**: Librería para generar documentos PDF
- **matplotlib**: Para gráficos adicionales (opcional)

## Verificar instalación

```bash
pip list | findstr reportlab
pip list | findstr matplotlib
```
