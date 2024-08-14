from playwright.sync_api import sync_playwright

def get_round_ids_for_tournament(page, tournament_id):
    round_ids = {}

    for round_number in range(1, 5):  # Adjust this range based on the possible number of rounds
        round_id = None

        def handle_request(route, request):
            nonlocal round_id
            url = request.url
            if "/api/v1/feat/stats/hole-stats-breakdown/" in url:
                round_id = url.split("/")[-2]  # Extract the round ID from the URL
                round_ids[round_number] = round_id
                print(f"Round {round_number} ID found: {round_id}")
            route.continue_()

        # Intercept network requests
        page.route("**/*", handle_request)

        # Navigate to the page and trigger a request by clicking on a hole
        page.goto(f'https://www.pdga.com/apps/tournament/live/event?eventId={tournament_id}&round={round_number}&division=MPO&view=CourseStats')

        try:
            page.click('div.table-row:nth-child(1)')
        except:
            print(f"No data available for round {round_number} in tournament {tournament_id}")
            continue

        page.wait_for_timeout(2000)  # Wait for requests to be processed

        # Stop intercepting requests
        page.unroute("**/*")

    return round_ids

def get_round_ids_for_all_tournaments(tournament_ids):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        tournament_round_ids = {}
        for tournament_id in tournament_ids:
            print(f"Processing Tournament ID: {tournament_id}")
            round_ids = get_round_ids_for_tournament(page, tournament_id)
            tournament_round_ids[tournament_id] = round_ids

        browser.close()
        return tournament_round_ids

# Running the function for a list of tournament IDs
tournaments = {'DGPT - All-Star Weekend - Doubles': '78584', 'DGPT - Chess.com Invitational presented by Discraft': '77775', 'DGPT+ Prodigy presents WACO': '77758', 'DGPT - The Open at Austin presented by Flight Factory Discs': '77759', "2024 United States Women's Disc Golf Championships presented by Mint Discs": '77091', 'DGPT - Texas State Disc Golf Championships - presented by Lone Star Disc': '77760', 'DGPT - Play It Again Sports Jonesboro Open - presented by Westside Discs': '77761', 'DGPT - Music City Open presented by Lone Star Disc': '77762', '2024 PDGA Champions Cup': '77099', 'DGPT - Dynamic Discs Open': '77763', 'DGPT - Copenhagen Open 2024': '78193', 'DGPT - OTB Open presented by MVP Disc Sports + WGE': '77764', 'DGPT+ 2024 Portland Open presented by Latitude64': '77765', 'DGPT - 2024 Beaver State Fling Presented by Innova': '77766', '2024 United States Amateur Disc Golf Championship': '77093', '2024 PDGA Professional Masters Disc Golf World Championships': '77133', '2024 PDGA Amateur Masters Disc Golf World Championships': '77094', 'DGPT - Turku Open powered by Prodigy': '78194', 'DGPT - The Preserve Championship connected by Microsoft Teams': '78271', 'DGPT - Swedish Open presented by Kastaplast': '78195', 'DGPT - Trubank Des Moines Challenge Presented by DGA': '77768', 'DGPT - Krokhol Open presented by Latitude 64': '78196', '2024 PDGA Junior Disc Golf World Championships': '77095', '2024 European Open presented by Discmania': '77750', 'DGPT - European Disc Golf Festival': '78197'}
# Replace with your tournament IDs
tournament_ids = []
for tournament, id in tournaments.items():
    tournament_ids.append(id)
round_ids = get_round_ids_for_all_tournaments(tournament_ids)
def remove_duplicate_rounds(tournament_round_ids):
    cleaned_round_ids = {}
    round_and_tournament_ids = {}
    for tournament_id, rounds in tournament_round_ids.items():
        # Create a reverse dictionary where keys are round IDs and values are the corresponding round numbers
        reverse_rounds = {}
        for round_number, round_id in rounds.items():
            if round_id not in reverse_rounds:
                reverse_rounds[round_id] = round_number

        # Recreate the dictionary with unique round IDs
        cleaned_round_ids[tournament_id] = {v: k for k, v in reverse_rounds.items()}
    return cleaned_round_ids

# Example usage:
cleaned_round_ids = remove_duplicate_rounds(round_ids)

print("Cleaned Round IDs for all tournaments:")
for tournament_id, rounds in cleaned_round_ids.items():
    print(f"Tournament {tournament_id}: {rounds}")

print(cleaned_round_ids)
