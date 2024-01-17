import pandas
from fpdf import FPDF

df = pandas.read_csv("articles.csv", dtype={"id":str})
print(df)


class Producto:
    def __init__(self, producto_id):
        self.id = producto_id
        self.name = df.loc[df["id"] == self.id, "name"].squeeze()
        self.precio = df.loc[df["id"] == self.id, "price"].squeeze()
        

    def disponible(self):
        disponible1 = self.stock = df.loc[df["id"] == self.id, "in stock"].squeeze()
        return disponible1 

class Recivo:
    def __init__(self, producto):
        self.producto = producto

    def generar(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.1", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Articulo: {self.producto.name}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Precio: {self.producto.precio}", ln=1)

        pdf.output("recivo.pdf")

        """Una vez hecho el recivo disminuimos el stock"""
        disponible1 = df.loc[df["id"] == self.producto.id, "in stock"].squeeze()
        disponible1 = disponible1 - 1
        df.loc[df["id"] == self.producto.id, "in stock"] = disponible1
        df.to_csv("articles.csv", index = False)


producto_ID = input("Proporcione el id del producto que desee adquirir: ")
producto_elegido = Producto(producto_ID)

if producto_elegido.disponible():

    resumen_de_compra = f"""
            Producto elegido: {producto_elegido.name}
            Precio: {producto_elegido.precio}
            Stock: {producto_elegido.stock}
            """
    print(resumen_de_compra)
    
    recivo = Recivo(producto_elegido)
    recivo.generar()
else:
    print("No hay articulos en stock")