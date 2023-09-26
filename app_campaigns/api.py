import frappe
import random


@frappe.whitelist()
def get_profile_ad():
    customer_profile_name = frappe.form_dict.get("customer_profile")
    position = frappe.form_dict.get("position")
    # Check if customer_profile_name is provided
    if not customer_profile_name:
        frappe.response["message"] = "Missing customer_profile parameter"
        frappe.local.response.http_status_code = 400
        return

    customer_profile = frappe.get_doc(
        "Customer Profile", customer_profile_name)

    # Check if customer_profile exists
    if not customer_profile:
        frappe.response["message"] = "Customer profile not found"
        frappe.local.response.http_status_code = 404
        return

    tags = customer_profile.get_tags()

    # Check if tags are available
    if not tags:
        frappe.response["message"] = "No tags found for the customer profile"
        frappe.local.response.http_status_code = 404
        return

    active_campaigns = frappe.get_all("Targeted Tags", filters=[
        ["tag", "in", tags]], fields=["parent"])
    unique_parents = list({campaign["parent"]
                          for campaign in active_campaigns})
    published_campaigns = frappe.get_all(
        "App Campaign", filters=[["workflow_state", "=", "Published"]])
    unique_active = list({campaign["name"]
                         for campaign in published_campaigns})
    unique_parents = list(set(unique_parents) & set(unique_active))
    # Check if there are no unique_parents
    if not unique_parents:
        frappe.response["message"] = "No active campaigns found"
        frappe.local.response.http_status_code = 404
        return

    ads = frappe.get_all("App Campaign Ads", filters=[["parent", "in", unique_parents], ["position", "=", position]], fields=[
                         "title", "name", "image", "weight", "description", "action_url", "position"])

    # Check if there are no ads
    if not ads:
        frappe.response["message"] = "No ads found for the active campaigns"
        frappe.local.response.http_status_code = 404
        return

    # Convert the "weight" values to floats and extract weights in one step
    weights = [float(item["weight"]) for item in ads]

    # Choose one object randomly based on their weights
    selected_item = random.choices(ads, weights=weights, k=1)[0]

    frappe.response["message"] = selected_item
    frappe.local.response.http_status_code = 200
