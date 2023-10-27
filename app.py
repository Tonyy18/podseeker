from lib import seleniumUtils, writer
from time import sleep
import json
import xlsxwriter
import traceback

writer.write_header()
writing_row = 1

f = open("keywords.txt")
keywords = f.read().strip().split("\n")
f.close()

selenium = seleniumUtils.Selenium()
selenium.get("https://app.podseeker.co/")


user_input = selenium.element_is_visible("#user_email")
pass_input = selenium.element_is_visible("#user_password")
user_input.send_keys("toni.isotalo@hotmail.com")
pass_input.send_keys("tonttu16")
selenium.element_is_visible("#kt-login_signin_submit").click()


selenium.element_is_visible("#select2-no_of_output-container").click()
ls = selenium.element_is_visible("#select2-no_of_output-results")
opts = selenium.get_all_from_element(ls, "li")
opts[len(opts) - 1].click()

emails_written = []
def get_data():
    try:
        selenium.elements_are_visible("#podCastModal")
        contact = selenium.get_elements("#podCastModal .contact-details")
        results = {}
        emails = []
        for e in contact:
            em = selenium.get_from_element(e, ".mb-2").get_attribute("innerText")
            sp = em.split(":")
            if(len(sp) > 1):
                email = sp[1].strip()
                if email != "" and email not in emails_written:
                    emails.append(email)
                    emails_written.append(email)
        
        results["emails"] = emails

        sub_headers = selenium.get_elements(".mb-3.mb-sm-0")
        for header in sub_headers:
            sub_title = selenium.get_from_element(header, ".show-sub-title")
            sub_value = selenium.get_from_element(header, ".show-sub-description")
            if(sub_title == None):
                continue
            sub_title = sub_title.get_attribute("innerText").lower().strip()
            if(sub_value):
                sub_value = sub_value.get_attribute("innerText").lower()
            if(sub_title == "genre"):
                results["genre"] = sub_value
            if(sub_title == "primary location"):
                results["location"] = sub_value
            if(sub_title == "latest episode"):
                results["latest_episode"] = sub_value
            if(sub_title == "episodes"):
                results["episodes_count"] = sub_value
            if(sub_title == "listeners"):
                listener_btn = selenium.get_from_element(header, ".listener-btn")
                if(listener_btn):
                    results["listeners"] = listener_btn.get_attribute("innerText")
            if(sub_title == "average apple rating"):
                stars_el = selenium.get_from_element(header, ".Stars")
                stars = 0
                if(stars_el):
                    stars = stars_el.get_attribute("style").split(":")[1].split(";")[0].strip()
                results["rating"] = stars
            if(sub_title == "estimated ad cost per episode"):
                divs = selenium.get_all_from_element(header, "div")
                cost = None
                if(len(divs) == 2):
                    cost = divs[1].get_attribute("innerText")
                results["ad_cost_per_episode"] = cost
            if(sub_title == "active"):
                divs = selenium.get_all_from_element(header, "div")
                active = None
                if(len(divs) == 2):
                    div = divs[1]
                    if(selenium.get_from_element(div, ".fa-times") != None):
                        active = "No"
                    if(selenium.get_from_element(div, ".fa-check-square")):
                        active = "Yes"
                results["active"] = active

            desc_el = selenium.get_element(".podcast-description-detail")
            desc = None
            if(desc_el):
                desc = desc_el.get_attribute("innerText")
            results["description"] = desc

            url_el = selenium.get_element(".podcast-url")
            url = None
            if(url_el):
                url = url_el.get_attribute("href")
            results["url"] = url

            episode_cards = selenium.execute_script("return document.getElementsByClassName('episode-details-card')")
            episodes = []
            for epi in episode_cards:
                epi_name = selenium.get_from_element(epi, "h6").get_attribute("innerText")
                epi_date = selenium.get_from_element(epi, ".text-muted").get_attribute("innerText")
                audio = selenium.get_from_element(epi, ".audio-player").get_attribute("data-audio")
                episodes.append({
                    "name": epi_name,
                    "date": epi_date,
                    "audio": audio
                })

            results["episodes"] = episodes
        title_el = selenium.get_element(".show-title")
        title = None
        if(title_el):
            title = title_el.get_attribute("innerText")
        results["title"] = title

        selenium.element_is_visible("#podCastModal button.close").click()
        return results
    except Exception:
        writer.workbook.close()
        print(traceback.format_exc())

cards_done = 0
keywords_used = []
try:
    for keyword in keywords:
        keyword = keyword.lower()
        if(keyword in keywords_used):
            continue
        selenium.scroll_to_top()
        search_input = selenium.element_is_visible("#podcast_search")
        search_input.clear()
        search_input.send_keys(keyword)
        while True:
            titles = selenium.elements_are_visible(".podcast-card .title")
            cards = selenium.execute_script("return document.getElementsByClassName('podcast-card')")
            if(len(cards) == 0):
                break
            for card in cards:
                try:
                    selenium.get_from_element(card, ".btn-blue-primary").click()
                except Exception as e:
                    continue
                selenium.driver.execute_script("$(arguments[0]).removeClass('podcast-card').hide()", card)
                data = get_data()
                new_row = writer.write_row(data, writing_row)
                writing_row = new_row + 1
                #print(json.dumps(data, indent=4))
                cards_done += 1
                print("Total email results: " + str(len(emails_written)))
                print("Cards: " + str(cards_done))

            selenium.scroll_to_bottom()
            try:
                selenium.execute_script("document.getElementById('load-more-podcasts').click()")
            except Exception as e:
                print(traceback.format_exc())
                break
        keywords_used.append(keyword)

except Exception:
    print(traceback.format_exc())
    writer.workbook.close()

selenium.scroll_to_top()
writer.workbook.close()

print()
print("Total email results: " + str(len(emails_written)))