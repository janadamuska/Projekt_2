import random

NUMBER_LENGTH: int = 4  # počet číslic tajného čísla


def print_intro() -> None:
    """Vypíše úvodní text hry Bulls & Cows."""
    print("Hi there!")
    print("-----------------------------------------------")
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print("-----------------------------------------------")
    print("Enter a number:")
    print("-----------------------------------------------")


def generate_secret_number() -> str:
    """Vygeneruje tajné čtyřciferné číslo s unikátními číslicemi, nezačínající nulou."""
    digits = list("0123456789")
    first_digit = random.choice(digits[1:])  # nesmí být '0'
    digits.remove(first_digit)
    other_digits = random.sample(digits, NUMBER_LENGTH - 1)
    secret = first_digit + "".join(other_digits)
    return secret


def validate_guess(guess: str) -> list[str]:
    """
    Zvaliduje uživatelský tip.
    Vrátí seznam chybových zpráv. Pokud je seznam prázdný, tip je platný.
    """
    errors: list[str] = []

    if len(guess) != NUMBER_LENGTH:
        errors.append(f"Number must have exactly {NUMBER_LENGTH} digits.")

    if not guess.isdigit():
        errors.append("You can only enter digits 0–9.")

    if guess and guess[0] == "0":
        errors.append("Number must not start with 0.")

    if len(set(guess)) != len(guess):
        errors.append("Digits must not repeat.")

    return errors


def count_bulls_and_cows(secret: str, guess: str) -> tuple[int, int]:
    """Vrátí počet bulls a cows pro daný tip."""
    bulls = 0

    # bulls = správná číslice na správné pozici
    for s, g in zip(secret, guess):
        if s == g:
            bulls += 1

    # správné číslice (bez ohledu na pozici)
    correct_digits = sum(1 for g in guess if g in secret)

    # cows = správné číslice, ale na jiné pozici
    cows = correct_digits - bulls

    return bulls, cows


def plural(count: int, singular: str, plural_form: str) -> str:
    """Vrátí správný tvar slova podle počtu (pro angličtinu)."""
    return singular if count == 1 else plural_form


def attempts_feedback(attempts: int) -> str:
    if attempts <= 4:
        return f"That's amazing! You did it in {attempts} attempts!"
    elif attempts <= 8:
        return f"Well done! You did it in {attempts} attempts!"
    else:
        return f"Good job! You did it in {attempts} attempts!"


def main() -> None:
    """Hlavní funkce hry Bulls & Cows."""
    print_intro()

    secret = generate_secret_number()

    attempts = 0

    while True:
        guess = input(">>> ").strip()
        print("-----------------------------------------------")

        errors = validate_guess(guess)
        if errors:
            print("Your guess is not valid:")
            for err in errors:
                print(" -", err)
            print("-----------------------------------------------")
            continue

        attempts += 1

        bulls, cows = count_bulls_and_cows(secret, guess)

        if bulls == NUMBER_LENGTH:
            print("Correct, you've guessed the right number")
            guess_word = plural(attempts, "guess", "guesses")
            print(f"in {attempts} {guess_word}!")
            print("-----------------------------------------------")

            print(attempts_feedback(attempts))
            return

        bull_word = plural(bulls, "bull", "bulls")
        cow_word = plural(cows, "cow", "cows")
        print(f"{bulls} {bull_word}, {cows} {cow_word}")
        print("-----------------------------------------------")


if __name__ == "__main__":
    main()