import pandas as pd

df = pd.read_excel(
    r'C:\Users\usuario\Documents\OfertaFlotaNoCubierta.xlsx',
    sheet_name='ConsolidadoNoCumplidos'
)

print("Nombres de columnas con códigos Unicode:")
print("=" * 80)
for i, col in enumerate(df.columns):
    unicode_codes = ' '.join([f'U+{ord(c):04X}' for c in col])
    print(f"{i}: {repr(col)}")
    print(f"   Unicode: {unicode_codes}")
    print()

print("\nPrimeras 5 filas de COD RUTA y RUTA:")
print(df[['COD RUTA', 'RUTA']].head(10))
