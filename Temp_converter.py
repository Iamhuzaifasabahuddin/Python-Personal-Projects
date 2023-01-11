def celsius_to_fahrenheit(temp: float):
    f = (temp * 9/5) + 32
    return f"Temperature of {temp} degree celsius to degrees fahrenheit is {f} "


def fahrenheit_to_celsius(temp: float):
    c = (temp - 32) * (5/9)
    return f"Temperature of {temp} degrees fahrenheit to degrees celsius is {c} degrees "


if __name__ == "__main__":
    while True:
        try:
            t = float(input("Enter temperature: "))
            print("celsius --> fahrenheit(F) or fahrenheit --> celsius(C)")
            convert = str(input("Enter which temperature you want to convert to: "))
            if convert.upper() not in ["F", "C"]:
                print("Please enter a valid conversion operation F or C")
            else:
                if convert.upper() == "F":
                    print(celsius_to_fahrenheit(t))
                elif convert.upper() == "C":
                    print(fahrenheit_to_celsius(t))
        except ValueError:
            print("Invalid temperature")
