import json
from datetime import datetime


OFFERS_FILE = "offers.json"
PRODUCTS_FILE = "products.json"
CUSTOMERS_FILE = "customers.json"



def load_data(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {filename}. Check file format.")
        return []


def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# TODO: Implementirajte funkciju za kreiranje nove ponude.
def create_new_offer(offers, products, customers):

    name = input("Unesite ime kupca: ")  

    while True:
        date_input = input("Unesite datum ponude (format YYYY-MM-DD): ")
        try:
            date = datetime.strptime(date_input, "%Y-%m-%d").date()
            break 
        except ValueError:
            print("Datum nije u ispravnom formatu. Pokušajte ponovno.")


    print("\nLista proizvoda:")
    for idx, prod in enumerate(products, start=1):
        print(f"{idx}. {prod['name']} - {prod['description']} - ${prod['price']}")

    items = []
    while True:
        prod_choice = input("Odaberite proizvod po broju (ili 'kraj' za završetak): ")
        if prod_choice.lower() == 'kraj':
            break
        try:
            prod_index = int(prod_choice) - 1
            if 0 <= prod_index < len(products):
                quantity = int(input(f"Unesite količinu za {products[prod_index]['name']}: "))
                item_total = products[prod_index]['price'] * quantity
                items.append({
                    "product_id": products[prod_index]['id'],
                    "product_name": products[prod_index]['name'],
                    "description": products[prod_index]['description'],
                    "quantity": quantity,
                    "price": products[prod_index]['price'],
                    "item_total": item_total
                })
            else:
                print("Neispravan izbor proizvoda. Pokušajte ponovno.")
        except ValueError:
            print("Neispravan unos. Pokušajte ponovno.")

    # --- 4. Izračun sub_total, tax i total ---
    sub_total = sum(item["item_total"] for item in items)
    tax = round(sub_total * 0.25, 2)  # PDV 25%
    total = round(sub_total + tax, 2)


    # --- 5. Kreiranje ponude ---
    offer_number = len(offers) + 1
    offer = {
        "offer_number": offer_number,
        "customer": {"name": name},
        "date": date_input,
        "items": items,
        "sub_total": sub_total,
        "tax": tax,
        "total": total
    }

    
    print("\n")
    print_offer(offer)

    offer_to_save = offer.copy()
    offer_to_save["customer"] = name

    offers.append(offer_to_save)
        
   
"""
    Prompt user to create a new offer by selecting a customer, entering date,
    choosing products, and calculating totals.
    """
    # Omogućite unos kupca
    # Izračunajte sub_total, tax i total
    # Dodajte novu ponudu u listu offers
    


# TODO: Implementirajte funkciju za upravljanje proizvodima.
def manage_products(products):
    while True:
        print("\nUpravljanje proizvodima:")
        print("1. Dodaj novi proizvod")
        print("2. Izmijeni postojeći proizvod")
        print("3. Povratak na glavni izbornik")
        choice = input("Odabrana opcija: ")

        if choice == "1":
            name = input("Unesite ime proizvoda: ")
            description = input("Unesite opis proizvoda: ")
            price = float(input("Unesite cijenu proizvoda: "))
            product_id = len(products) + 1
            product = {
                "id": product_id,
                "name": name,
                "description": description,
                "price": price
            }
            products.append(product)
            save_data(PRODUCTS_FILE, products)
            print("\n\nProizvod uspješno dodan.\n\n")
        elif choice == "2":
            for idx, prod in enumerate(products, start=1):
                print(f"{idx}. {prod['name']} - {prod['description']} - ${prod['price']}")
            prod_choice = int(input("Odaberite proizvod za izmjenu po broju: ")) - 1
            if 0 <= prod_choice < len(products):
                name = input(f"Unesite novo ime proizvoda ({products[prod_choice]['name']}): ") or products[prod_choice]['name']
                description = input(f"Unesite novi opis proizvoda ({products[prod_choice]['description']}): ") or products[prod_choice]['description']
                price_input = input(f"Unesite novu cijenu proizvoda ({products[prod_choice]['price']}): ")
                price = float(price_input) if price_input else products[prod_choice]['price']
                
                products[prod_choice].update({
                    "name": name,
                    "description": description,
                    "price": price
                })
                save_data(PRODUCTS_FILE, products)
                print("\n\nProizvod uspješno izmijenjen.\n\n")
            else:
                print("Neispravan izbor proizvoda.")
        elif choice == "3":
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")

    """
    Allows the user to add a new product or modify an existing product.
    """
    # Omogućite korisniku izbor između dodavanja ili izmjene proizvoda
    # Za dodavanje: unesite podatke o proizvodu i dodajte ga u listu products
    # Za izmjenu: selektirajte proizvod i ažurirajte podatke



# TODO: Implementirajte funkciju za upravljanje kupcima.    
def manage_customers(customers):
    while True:
        print("\n\nUpravljanje korisnicima:\n")
        print("1. Dodaj novog kupca")
        print("2. Pregled svih kupaca")
        print("3. Povratak na glavni izbornik")
        choice = input("Odabrana opcija: ")

        if choice == "1":
            name = input("Unesite ime kupca: ")
            email = input("Unesite email kupca: ")
            vat_id = input("Unesite VAT ID kupca (može ostati prazno): ")
            customer = {
                "name": name,
                "email": email,
                "vat_id": vat_id
            }
            customers.append(customer)
            save_data(CUSTOMERS_FILE, customers)
            print(f"\n Kupac '{name}' uspješno dodan.\n")

        elif choice == "2":
            print("\n\nLista kupaca:\n")
            customers = load_data(CUSTOMERS_FILE)
            if not customers:
                print("Nema unesenih kupaca.")
            else:
                for idx, cust in enumerate(customers, start=1):
                    print(f"{idx}. {cust['name']} - {cust['email']} - VAT ID: {cust['vat_id']}")

        elif choice == "3":
            break

        else:
            print("Neispravan izbor. Pokušajte ponovno.")


    """
    Allows the user to add a new customer or view all customers.
    """
    # Za dodavanje: omogući unos imena kupca, emaila i unos VAT ID-a
    # Za pregled: prikaži listu svih kupaca
    


# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers(offers):
     
     while True:
        print("\n\nPregled ponuda:\n")
        print("1. Prikaži sve ponude")
        print("2. Prikaži ponude za određeni mjesec")
        print("3. Prikaži pojedinačnu ponudu po broju ponude")
        print("4. Povratak na glavni izbornik")

        choice = input("Odaberi opciju: ")

        if choice == "1":
            offers = load_data(OFFERS_FILE)  # učitaj sve ponude iz JSON-a
            if not offers:
                print("Nema unesenih ponuda.")
            else:
                print("\n\n--- Sve ponude ---\n")
            for offer in offers:
            # osiguraj da je customer rječnik s 'name'
                if isinstance(offer["customer"], str):
                    offer["customer"] = {"name": offer["customer"]}
                    print_offer(offer)
                    print("\n""\n")
            
        if choice == "2":
            month_input = input("Unesite mjesec i godinu (MM-YYYY): ")
            try:
                month, year = map(int, month_input.split("-"))
                filtered_offers = [
                    offer for offer in offers
                    if datetime.strptime(offer["date"], "%Y-%m-%d").month == month and
                       datetime.strptime(offer["date"], "%Y-%m-%d").year == year
                ]
                if not filtered_offers:
                    print(f"Nema ponuda za {month_input}.")
                else:
                    print(f"\n\n--- Ponude za {month_input} ---\n")
                    for offer in filtered_offers:
                        print_offer(offer)
                        print("\n""\n")
            except ValueError:
                print("Neispravan format. Pokušajte ponovno.")
        elif choice == "3":
            offer_num_input = input("Unesite broj ponude: ")
            try:
                offer_num = int(offer_num_input)
                selected_offer = next((offer for offer in offers if offer["offer_number"] == offer_num), None)
                if not selected_offer:
                    print(f"Ponuda broj {offer_num} nije pronađena.")
                else:
                    print(f"\n\n--- Ponuda broj {offer_num} ---\n")
                    print_offer(selected_offer)
                    print("\n""\n")
            except ValueError:
                print("Neispravan unos. Pokušajte ponovno.")

        elif choice == "4":
        
         break

            
        

    
    




"""
Display all offers, offers for a selected month, or a single offer by ID.
"""
# Omogućite izbor pregleda: sve ponude, po mjesecu ili pojedinačna ponuda
# Prikaz relevantnih ponuda na temelju izbora



# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer):
    """Display details of a single offer."""
    print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']['name']}, Datum ponude: {offer['date']}")
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
    print(f"Ukupno: ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno za platiti: ${offer['total']}")


def main():
    # Učitavanje podataka iz JSON datoteka
    offers = load_data(OFFERS_FILE)
    products = load_data(PRODUCTS_FILE)
    customers = load_data(CUSTOMERS_FILE)

    while True:
        print("\nOffers Calculator izbornik:")
        print("1. Kreiraj novu ponudu")
        print("2. Upravljanje proizvodima")
        print("3. Upravljanje korisnicima")
        print("4. Prikaz ponuda")
        print("5. Izlaz")
        choice = input("Odabrana opcija: ")

        if choice == "1":
            create_new_offer(offers, products, customers)
        elif choice == "2":
            manage_products(products)
        elif choice == "3":
            manage_customers(customers)
        elif choice == "4":
            display_offers(offers)
        elif choice == "5":
            # Pohrana podataka prilikom izlaza
            save_data(OFFERS_FILE, offers)
            save_data(PRODUCTS_FILE, products)
            save_data(CUSTOMERS_FILE, customers)
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")


if __name__ == "__main__":
    main()