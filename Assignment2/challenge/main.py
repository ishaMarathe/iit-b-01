import sys
from math_utils import rect_area, sqr_area, circ_area
from jsonplaceholder import fetch_json_data
from weatherapp import get_current_weather, pretty_print_weather


def main_menu():
    print("\n=== MAIN MENU ===")
    print("1.Area Calculations")
    print("2.Fetch JSONPlaceholder Posts")
    print("3.Weather App")
    print("4.Exit")


def area_menu():
    print("\n--- AREA CALCULATIONS ---")
    print("1.Rectangle")
    print("2.Square")
    print("3.Circle")
    print("4.Back")


def area_driver():
    while True:
        area_menu()
        choice=input("Choice:")


        try:
            if choice=="1":
                l=float(input("Length:"))
                b=float(input("Breadth:"))
                print("Area =",rect_area(l,b))

            elif choice=="2":
                s=float(input("Side:"))
                print("Area =",sqr_area(s))

            elif choice == "3":
                r=float(input("Radius:"))
                print("Area =",circ_area(r))

            elif choice=="4":
                return 

            else:
                print("Invalid choice!")

        except Exception as e:
            print("Error:",e)


def fetch_data_driver():
    print("\nFetching JSONPlaceholder posts")
    try:
        fetch_json_data()
    except Exception as e:
        print("Error:",e)


def weather_driver():
    city=input("\nEnter city: ")
    try:
        data = get_current_weather(city)
        pretty_print_weather(data)
    except Exception as e:
        print("Error:",e)


def main():
    while True:
        main_menu()
        choice = input("Choice: ")

        if choice=="1":
            area_driver()
        elif choice=="2":
            fetch_data_driver()
        elif choice=="3":
            weather_driver()
        elif choice=="4":
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
