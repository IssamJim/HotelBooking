import pandas

df = pandas.read_csv("hotels.csv", dtype={"id":str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Reservar un hotel cambiando su disponibilidad a no"""
        
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Vemos si el hotel esta disponible"""

        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class Spa(Hotel):
    def reservation(self, nombre):
        content = f"""
        Gracias por su reservacion con Spa!
        Nombre: {nombre}
        Hotel: {self.name}
        """
        print(content)


class ReservationTicket: 
    def __init__(self, customer_name, hotel_obj):
        self.customer_name = customer_name
        self.hotel = hotel_obj

    def generate(self):
        content = f"""
        Gracias por su reservacion!
        Nombre: {self.customer_name}
        Hotel: {self.hotel.name}        
        """
        return content


class CreditCard:
    def __init__(self,number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number":self.number, "expiration":expiration, "holder":holder, "cvc":cvc}
        if card_data in df_cards:
            return True
        

class SecureCreditCard(CreditCard):

    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"]
        if not password.empty:  # Verificar si se encontró alguna contraseña para el número de tarjeta
            password = password.squeeze()
            if password == given_password:
                return True
        return False


print(df)
hotel_ID = input("Proporcione el id del hotel: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number="1234")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Nombre: ")
            Reservation_ticket = ReservationTicket(customer_name = name, hotel_obj=hotel)
            print(Reservation_ticket.generate())
            spaReservation = input("Desea agregar un paquete de Spa? ")
            spaRservado = Spa(hotel_ID)
            if spaReservation == "si":
               spaRservado.reservation(nombre=name)

            else:
                print("Gracias por su tiempo")
        else:
            print("Autentificacion de tarjeta fallo")
    else:
        print("Problema al pagar la reservacion.")
else:
    print("Hotel is not available.")