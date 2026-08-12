import os
import sys
import json
import random
import time
import shutil
import termios
import tty

# ============================================================
# HIGH STAKES BLACKJACK 4
#
# DEAL -> BET -> SWAP -> HIT/STAND -> REVEAL -> RESULT -> SHOP
#
# New:
# - Empty inventory at start
# - Arcade initials for high scores
# - T = Tutorial
# ============================================================

STARTING_MONEY = 500.0
SCORE_FILE = os.path.expanduser("~/highstakes_scores.json")

RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"

SUITS = ["♠", "♥", "♦", "♣"]

RANKS = [
    "2", "3", "4", "5", "6", "7",
    "8", "9", "10", "J", "Q", "K", "A"
]


# ============================================================
# TERMINAL
# ============================================================

def terminal_size():
    return shutil.get_terminal_size((120, 40))


def clear():
    os.system("clear")


def strip_ansi(text):
    for code in [
        RESET, BOLD, RED, GREEN, YELLOW, BLUE,
        MAGENTA, CYAN, WHITE, GRAY
    ]:
        text = text.replace(code, "")
    return text


def center_text(text):
    width, _ = terminal_size()
    plain = strip_ansi(text)
    padding = max(0, (width - len(plain)) // 2)
    return " " * padding + text


def cprint(text=""):
    print(center_text(text))


def wait_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    return key


def pause():
    input(center_text("Press ENTER to continue..."))


def vertical_space():
    _, height = terminal_size()
    amount = max(1, (height - 30) // 2)

    for _ in range(amount):
        print()


# ============================================================
# MONEY
# ============================================================

def parse_money(text):

    text = text.strip().lower()
    text = text.replace("$", "")
    text = text.replace(",", "")

    if not text:
        return None

    multiplier = 1

    if text.endswith("k"):
        multiplier = 1000
        text = text[:-1]

    elif text.endswith("m"):
        multiplier = 1_000_000
        text = text[:-1]

    try:
        return float(text) * multiplier
    except ValueError:
        return None


# ============================================================
# SCORES
# ============================================================

def load_scores():

    if not os.path.exists(SCORE_FILE):
        return []

    try:
        with open(SCORE_FILE, "r") as f:
            scores = json.load(f)

        if isinstance(scores, list):
            return scores

    except Exception:
        pass

    return []


def save_scores(scores):

    try:
        with open(SCORE_FILE, "w") as f:
            json.dump(scores[:3], f)

    except Exception:
        pass


def add_high_score(score):

    scores = load_scores()

    entry = {
        "initials": get_initials(),
        "score": round(score, 2)
    }

    scores.append(entry)

    scores.sort(
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    scores = scores[:3]

    save_scores(scores)


def get_initials():

    clear()

    vertical_space()

    cprint(
        CYAN + BOLD +
        "╔════════════════════════════════════════════════════════╗"
        + RESET
    )

    cprint(
        "║                    NEW HIGH SCORE!                     ║"
    )

    cprint(
        CYAN + BOLD +
        "╚════════════════════════════════════════════════════════╝"
        + RESET
    )

    print()

    cprint(
        YELLOW +
        "ENTER YOUR 3 LETTER ARCADE INITIALS" +
        RESET
    )

    print()

    while True:

        initials = input(
            center_text(
                "> "
            )
        ).strip().upper()

        initials = "".join(
            c for c in initials
            if c.isalpha()
        )

        if len(initials) == 3:
            return initials

        cprint(
            RED +
            "Please enter exactly 3 letters." +
            RESET
        )


# ============================================================
# TUTORIAL
# ============================================================

def tutorial():

    while True:

        clear()

        vertical_space()

        cprint(
            CYAN + BOLD +
            "╔════════════════════════════════════════════════════════╗"
            + RESET
        )

        cprint(
            "║                 HOW TO PLAY                            ║"
        )

        cprint(
            CYAN + BOLD +
            "╚════════════════════════════════════════════════════════╝"
            + RESET
        )

        print()

        cprint(
            YELLOW + BOLD +
            "1. DEAL" +
            RESET
        )

        cprint(
            "You receive two cards and see the dealer's cards."
        )

        print()

        cprint(
            YELLOW + BOLD +
            "2. BET" +
            RESET
        )

        cprint(
            "Place your wager AFTER seeing your starting cards."
        )

        cprint(
            "You can type things like:"
        )

        cprint(
            "500     1k     2.5k     10k"
        )

        print()

        cprint(
            YELLOW + BOLD +
            "3. SWAP" +
            RESET
        )

        cprint(
            "Between betting and hitting, you can use stored cards."
        )

        cprint(
            "Your inventory starts EMPTY."
        )

        cprint(
            "Cards bought from the shop can replace cards in your hand."
        )

        print()

        cprint(
            YELLOW + BOLD +
            "4. HIT / STAND" +
            RESET
        )

        cprint(
            "Press H to hit."
        )

        cprint(
            "Press S to stand."
        )

        cprint(
            "No ENTER key is needed."
        )

        print()

        cprint(
            YELLOW + BOLD +
            "5. REVEAL" +
            RESET
        )

        cprint(
            "The dealer reveals the hidden card."
        )

        cprint(
            "Dealer hits until reaching at least 17."
        )

        print()

        cprint(
            YELLOW + BOLD +
            "6. SHOP" +
            RESET
        )

        cprint(
            "After the round, you can buy cards."
        )

        cprint(
            "You have three inventory slots."
        )

        cprint(
            "Cards become stronger and more expensive."
        )

        print()

        cprint(
            GREEN + BOLD +
            "BLACKJACK = ACE + 10/VALUE CARD" +
            RESET
        )

        cprint(
            "Blackjack pays 3:2."
        )

        print()

        cprint(
            MAGENTA +
            "Press T again to return to the title screen." +
            RESET
        )

        key = wait_key().lower()

        if key == "t":
            return


# ============================================================
# TITLE
# ============================================================

def title_screen():

    while True:

        scores = load_scores()

        clear()

        vertical_space()

        cprint(
            CYAN + BOLD +
            "╔════════════════════════════════════════════════════════╗"
            + RESET
        )

        cprint(
            "║                                                        ║"
        )

        cprint(
            "║              ♠ BLACKJACK ♠                             ║"
        )

        cprint(
            "║                 HIGH STAKES                            ║"
        )

        cprint(
            "║                                                        ║"
        )

        cprint(
            CYAN + BOLD +
            "╠════════════════════════════════════════════════════════╣"
            + RESET
        )

        cprint(
            MAGENTA + BOLD +
            "║                 TOP SCORES                            ║"
            + RESET
        )

        for i in range(3):

            if i < len(scores):

                initials = scores[i].get(
                    "initials",
                    "???"
                )

                score = scores[i].get(
                    "score",
                    0
                )

                text = f"{i + 1}. {initials}   ${score:,.2f}"

            else:

                text = f"{i + 1}. ---   ---"

            cprint(
                f"║             {text:<35}║"
            )

        cprint(
            CYAN + BOLD +
            "╠════════════════════════════════════════════════════════╣"
            + RESET
        )

        cprint(
            f"║              STARTING BANKROLL: $500                  ║"
        )

        cprint(
            "║                                                        ║"
        )

        cprint(
            GREEN + BOLD +
            "║                 [ SPACE ] PLAY                         ║"
            + RESET
        )

        cprint(
            YELLOW +
            "║                    [ T ] TUTORIAL                      ║"
            + RESET
        )

        cprint(
            RED +
            "║                     [ Q ] QUIT                         ║"
            + RESET
        )

        cprint(
            CYAN + BOLD +
            "╚════════════════════════════════════════════════════════╝"
            + RESET
        )

        key = wait_key().lower()

        if key == " ":
            return True

        if key == "t":
            tutorial()

        elif key == "q":
            return False


# ============================================================
# CARDS
# ============================================================

def new_deck():

    deck = []

    for suit in SUITS:
        for rank in RANKS:
            deck.append((rank, suit))

    random.shuffle(deck)

    return deck


def card_value(card):

    rank = card[0]

    if rank in ["J", "Q", "K"]:
        return 10

    if rank == "A":
        return 11

    return int(rank)


def hand_value(hand):

    value = 0
    aces = 0

    for card in hand:

        value += card_value(card)

        if card[0] == "A":
            aces += 1

    while value > 21 and aces:

        value -= 10
        aces -= 1

    return value


def is_blackjack(hand):

    return len(hand) == 2 and hand_value(hand) == 21


# ============================================================
# CARD DISPLAY
# ============================================================

def card_lines(card, hidden=False):

    if hidden:

        return [
            "┌─────────┐",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "└─────────┘"
        ]

    rank, suit = card

    color = (
        RED
        if suit in ["♥", "♦"]
        else WHITE
    )

    return [
        "┌─────────┐",
        f"│ {rank:<2}      │",
        "│         │",
        f"│    {color}{suit}{RESET}    │",
        "│         │",
        f"│      {rank:>2} │",
        "│         │",
        "└─────────┘"
    ]


def show_cards(cards, hide_first=False):

    if not cards:
        return

    rendered = []

    for i, card in enumerate(cards):

        rendered.append(
            card_lines(
                card,
                hide_first and i == 0
            )
        )

    for row in range(8):

        line = "     ".join(
            card[row]
            for card in rendered
        )

        cprint(line)


# ============================================================
# TABLE
# ============================================================

def show_table(
    player,
    dealer,
    bankroll,
    bet=0,
    hide_dealer=True,
    message=""
):

    clear()

    vertical_space()

    cprint(
        CYAN + BOLD +
        "╔════════════════════════════════════════════════════════╗"
        + RESET
    )

    cprint(
        "║              ♠ BLACKJACK — HIGH STAKES                ║"
    )

    cprint(
        CYAN + BOLD +
        "╚════════════════════════════════════════════════════════╝"
        + RESET
    )

    print()

    cprint(
        YELLOW +
        f"💰 BANKROLL: ${bankroll:,.2f}" +
        RESET
    )

    if bet:

        cprint(
            YELLOW +
            f"🎲 BET: ${bet:,.2f}" +
            RESET
        )

    print()

    cprint(
        MAGENTA + BOLD +
        "DEALER" +
        RESET
    )

    print()

    show_cards(
        dealer,
        hide_first=hide_dealer
    )

    print()

    cprint(
        GREEN + BOLD +
        "YOU" +
        RESET
    )

    print()

    show_cards(player)

    print()

    if player:

        cprint(
            YELLOW +
            f"Your value: {hand_value(player)}" +
            RESET
        )

    if message:

        print()

        cprint(
            CYAN +
            message +
            RESET
        )


# ============================================================
# DEAL
# ============================================================

def deal_round(deck):

    player = [
        deck.pop(),
        deck.pop()
    ]

    dealer = [
        deck.pop(),
        deck.pop()
    ]

    return player, dealer


# ============================================================
# BET
# ============================================================

def betting_phase(
    player,
    dealer,
    bankroll
):

    while True:

        show_table(
            player,
            dealer,
            bankroll,
            hide_dealer=True,
            message="You see your cards. Place your bet."
        )

        print()

        cprint(
            CYAN + BOLD +
            "PLACE YOUR BET" +
            RESET
        )

        cprint(
            "Examples: 500   1k   2.5k   10k"
        )

        print()

        amount = input(
            center_text(
                YELLOW +
                "Bet: $" +
                RESET
            )
        )

        if amount.strip().lower() == "all":
            return bankroll

        bet = parse_money(amount)

        if bet is None:

            cprint(
                RED +
                "Invalid bet." +
                RESET
            )

            time.sleep(1)
            continue

        if bet <= 0:

            cprint(
                RED +
                "Bet must be greater than $0." +
                RESET
            )

            time.sleep(1)
            continue

        if bet > bankroll:

            cprint(
                RED +
                "You don't have enough money." +
                RESET
            )

            time.sleep(1)
            continue

        return bet


# ============================================================
# SWAP
# ============================================================

def swap_phase(
    player,
    storage,
    bankroll,
    bet
):

    # Empty inventory means no swap phase.
    if not storage:

        show_table(
            player,
            [],
            bankroll,
            bet,
            hide_dealer=False,
            message="Your inventory is empty."
        )

        time.sleep(1.5)

        return

    while True:

        show_table(
            player,
            [],
            bankroll,
            bet,
            hide_dealer=False,
            message="SWAP PHASE"
        )

        print()

        cprint(
            MAGENTA + BOLD +
            "STORED CARDS" +
            RESET
        )

        print()

        for i, card in enumerate(storage):

            cprint(
                f"[{i + 1}] {card[0]}{card[1]}"
            )

        print()

        cprint(
            "Choose a stored card."
        )

        cprint(
            "Then choose a hand card to replace."
        )

        cprint(
            "Press ENTER when finished."
        )

        choice = input(
            center_text(
                YELLOW +
                "Swap > " +
                RESET
            )
        ).strip()

        if choice == "":
            return

        if choice not in ["1", "2", "3"]:

            cprint(
                RED +
                "Invalid stored-card slot." +
                RESET
            )

            time.sleep(1)
            continue

        storage_index = int(choice) - 1

        if storage_index >= len(storage):
            continue

        hand_choice = input(
            center_text(
                YELLOW +
                "Replace hand card 1 or 2: " +
                RESET
            )
        ).strip()

        if hand_choice not in ["1", "2"]:

            cprint(
                RED +
                "Invalid hand card." +
                RESET
            )

            time.sleep(1)
            continue

        hand_index = int(hand_choice) - 1

        player[hand_index], storage[storage_index] = (
            storage[storage_index],
            player[hand_index]
        )

        cprint(
            GREEN +
            "Cards swapped!" +
            RESET
        )

        time.sleep(1)


# ============================================================
# PLAYER TURN
# ============================================================

def player_turn(
    player,
    dealer,
    deck,
    bankroll,
    bet
):

    while True:

        show_table(
            player,
            dealer,
            bankroll,
            bet,
            hide_dealer=True
        )

        print()

        value = hand_value(player)

        if value > 21:

            cprint(
                RED + BOLD +
                "💥 BUST!" +
                RESET
            )

            return "bust"

        if value == 21:

            cprint(
                GREEN + BOLD +
                "21!" +
                RESET
            )

            return "stand"

        cprint(
            YELLOW + BOLD +
            "[H] HIT        [S] STAND" +
            RESET
        )

        key = wait_key().lower()

        if key == "h":

            player.append(
                deck.pop()
            )

        elif key == "s":

            return "stand"


# ============================================================
# DEALER
# ============================================================

def dealer_turn(
    player,
    dealer,
    deck,
    bankroll,
    bet
):

    show_table(
        player,
        dealer,
        bankroll,
        bet,
        hide_dealer=False,
        message="Dealer reveals the hole card."
    )

    time.sleep(1.5)

    while hand_value(dealer) < 17:

        dealer.append(
            deck.pop()
        )

        show_table(
            player,
            dealer,
            bankroll,
            bet,
            hide_dealer=False,
            message="Dealer hits..."
        )

        time.sleep(1.2)


# ============================================================
# SHOP
# ============================================================

def shop_cards(round_number):

    tier = min(
        (round_number - 1) // 2,
        3
    )

    tiers = [
        ["2", "3", "4"],
        ["5", "6", "7"],
        ["8", "9", "10"],
        ["J", "Q", "K", "A"]
    ]

    available = tiers[tier]

    return random.sample(
        available,
        min(3, len(available))
    )


def shop_price(rank):

    prices = {
        "2": 500,
        "3": 600,
        "4": 700,
        "5": 800,
        "6": 900,
        "7": 1000,
        "8": 1100,
        "9": 1200,
        "10": 1300,
        "J": 1400,
        "Q": 1500,
        "K": 1600,
        "A": 1700
    }

    return prices[rank]


def shop_phase(
    bankroll,
    storage,
    round_number
):

    cards = shop_cards(round_number)

    while True:

        clear()

        vertical_space()

        cprint(
            CYAN + BOLD +
            "╔════════════════════════════════════════════════════════╗"
            + RESET
        )

        cprint(
            "║                    CARD SHOP                           ║"
        )

        cprint(
            CYAN + BOLD +
            "╚════════════════════════════════════════════════════════╝"
            + RESET
        )

        print()

        cprint(
            YELLOW +
            f"💰 BANKROLL: ${bankroll:,.2f}" +
            RESET
        )

        print()

        cprint(
            MAGENTA + BOLD +
            "AVAILABLE CARDS" +
            RESET
        )

        print()

        for i, rank in enumerate(cards):

            cprint(
                f"[{i + 1}] {rank:<2} — ${shop_price(rank):,.0f}"
            )

        print()

        cprint(
            GREEN + BOLD +
            "YOUR INVENTORY" +
            RESET
        )

        if not storage:

            cprint(
                GRAY +
                "EMPTY" +
                RESET
            )

        else:

            for i, card in enumerate(storage):

                cprint(
                    f"[{i + 1}] {card[0]}{card[1]}"
                )

        print()

        cprint(
            "Choose a shop card."
        )

        cprint(
            "Then choose an inventory slot to replace."
        )

        cprint(
            "Press ENTER to leave."
        )

        choice = input(
            center_text(
                YELLOW +
                "Shop > " +
                RESET
            )
        ).strip()

        if choice == "":
            return bankroll, storage

        if choice not in ["1", "2", "3"]:

            cprint(
                RED +
                "Invalid shop choice." +
                RESET
            )

            time.sleep(1)
            continue

        rank = cards[int(choice) - 1]
        price = shop_price(rank)

        if bankroll < price:

            cprint(
                RED +
                "You cannot afford that card." +
                RESET
            )

            time.sleep(1)
            continue

        # ----------------------------------------------------
        # EMPTY INVENTORY
        # ----------------------------------------------------

        if len(storage) < 3:

            slot = len(storage) + 1

            bankroll -= price

            suit = random.choice(SUITS)

            storage.append(
                (rank, suit)
            )

            cprint(
                GREEN +
                f"Bought {rank} for ${price:,.0f}!" +
                RESET
            )

            cprint(
                f"Added to inventory slot {slot}."
            )

            time.sleep(1.5)

            cards = shop_cards(round_number)

            continue

        # ----------------------------------------------------
        # FULL INVENTORY
        # ----------------------------------------------------

        cprint(
            YELLOW +
            "Inventory full! Choose a slot to replace." +
            RESET
        )

        slot = input(
            center_text(
                "Replace slot 1, 2, or 3: "
            )
        ).strip()

        if slot not in ["1", "2", "3"]:

            cprint(
                RED +
                "Invalid slot." +
                RESET
            )

            time.sleep(1)
            continue

        slot_index = int(slot) - 1

        old_card = storage[slot_index]

        bankroll -= price

        suit = random.choice(SUITS)

        storage[slot_index] = (
            rank,
            suit
        )

        cprint(
            GREEN +
            f"Bought {rank} for ${price:,.0f}!" +
            RESET
        )

        cprint(
            f"Replaced {old_card[0]}{old_card[1]}."
        )

        time.sleep(1.5)

        cards = shop_cards(round_number)


# ============================================================
# RESULT
# ============================================================

def resolve_round(
    player,
    dealer,
    bankroll,
    bet
):

    show_table(
        player,
        dealer,
        bankroll,
        bet,
        hide_dealer=False
    )

    player_score = hand_value(player)
    dealer_score = hand_value(dealer)

    print()

    if player_score > 21:

        cprint(
            RED + BOLD +
            f"💀 YOU BUST — LOSE ${bet:,.2f}" +
            RESET
        )

        return bankroll

    if dealer_score > 21:

        bankroll += bet * 2

        cprint(
            GREEN + BOLD +
            f"🎉 DEALER BUSTS — WIN ${bet:,.2f}!" +
            RESET
        )

        return bankroll

    if player_score > dealer_score:

        bankroll += bet * 2

        cprint(
            GREEN + BOLD +
            f"🎉 YOU WIN ${bet:,.2f}!" +
            RESET
        )

        return bankroll

    if player_score < dealer_score:

        cprint(
            RED + BOLD +
            f"💀 DEALER WINS — LOSE ${bet:,.2f}" +
            RESET
        )

        return bankroll

    bankroll += bet

    cprint(
        YELLOW + BOLD +
        "🤝 PUSH — BET RETURNED" +
        RESET
    )

    return bankroll


# ============================================================
# GAME OVER
# ============================================================

def game_over(
    high_score
):

    clear()

    vertical_space()

    cprint(
        RED + BOLD +
        "╔════════════════════════════════════════════════════════╗"
        + RESET
    )

    cprint(
        "║                    GAME OVER                           ║"
    )

    cprint(
        RED + BOLD +
        "║                  💸 YOU'RE BROKE 💸                    ║"
        + RESET
    )

    cprint(
        RED + BOLD +
        "╚════════════════════════════════════════════════════════╝"
        + RESET
    )

    print()

    cprint(
        YELLOW + BOLD +
        f"RUN HIGH SCORE: ${high_score:,.2f}" +
        RESET
    )

    print()

    add_high_score(high_score)

    cprint(
        GREEN +
        "Score saved to the arcade leaderboard!" +
        RESET
    )

    print()

    cprint(
        "Press ENTER to return to the title screen."
    )

    input()


# ============================================================
# MAIN
# ============================================================

def main():

    if not title_screen():

        clear()

        cprint(
            CYAN +
            "Thanks for playing." +
            RESET
        )

        return

    bankroll = STARTING_MONEY
    high_score = STARTING_MONEY

    # IMPORTANT:
    # You start with NOTHING.
    storage = []

    round_number = 1

    while bankroll > 0:

        deck = new_deck()

        # ----------------------------------------------------
        # DEAL
        # ----------------------------------------------------

        player, dealer = deal_round(deck)

        # ----------------------------------------------------
        # BET
        # ----------------------------------------------------

        bet = betting_phase(
            player,
            dealer,
            bankroll
        )

        bankroll -= bet

        # ----------------------------------------------------
        # SWAP
        # ----------------------------------------------------

        swap_phase(
            player,
            storage,
            bankroll,
            bet
        )

        # ----------------------------------------------------
        # BLACKJACK
        # ----------------------------------------------------

        if is_blackjack(player):

            show_table(
                player,
                dealer,
                bankroll,
                bet,
                hide_dealer=True,
                message="BLACKJACK!"
            )

            time.sleep(1)

            if is_blackjack(dealer):

                bankroll += bet

                cprint(
                    YELLOW +
                    "PUSH — BOTH HAVE BLACKJACK." +
                    RESET
                )

            else:

                winnings = bet * 1.5

                bankroll += bet + winnings

                cprint(
                    GREEN + BOLD +
                    f"🃏 BLACKJACK! +${winnings:,.2f}" +
                    RESET
                )

        else:

            result = player_turn(
                player,
                dealer,
                deck,
                bankroll,
                bet
            )

            if result == "stand":

                dealer_turn(
                    player,
                    dealer,
                    deck,
                    bankroll,
                    bet
                )

                bankroll = resolve_round(
                    player,
                    dealer,
                    bankroll,
                    bet
                )

            else:

                show_table(
                    player,
                    dealer,
                    bankroll,
                    bet,
                    hide_dealer=False,
                    message="You busted."
                )

        # ----------------------------------------------------
        # HIGH SCORE
        # ----------------------------------------------------

        if bankroll > high_score:
            high_score = bankroll

        print()

        cprint(
            YELLOW +
            f"CURRENT BANKROLL: ${bankroll:,.2f}" +
            RESET
        )

        cprint(
            CYAN +
            f"RUN HIGH SCORE: ${high_score:,.2f}" +
            RESET
        )

        pause()

        # ----------------------------------------------------
        # GAME OVER
        # ----------------------------------------------------

        if bankroll <= 0:

            game_over(
                high_score
            )

            return

        # ----------------------------------------------------
        # SHOP
        # ----------------------------------------------------

        bankroll, storage = shop_phase(
            bankroll,
            storage,
            round_number
        )

        if bankroll > high_score:
            high_score = bankroll

        round_number += 1

        clear()

        vertical_space()

        cprint(
            GREEN + BOLD +
            f"ROUND {round_number}" +
            RESET
        )

        cprint(
            f"Bankroll: ${bankroll:,.2f}"
        )

        cprint(
            f"Run High Score: ${high_score:,.2f}"
        )

        print()

        cprint(
            "[ENTER] Next round"
        )

        cprint(
            "[Q] Quit"
        )

        choice = input().strip().lower()

        if choice == "q":

            add_high_score(high_score)

            clear()

            cprint(
                CYAN + BOLD +
                "You walked away from the table." +
                RESET
            )

            cprint(
                YELLOW +
                f"🏆 Highest bankroll: ${high_score:,.2f}" +
                RESET
            )

            return


if __name__ == "__main__":
    main()
