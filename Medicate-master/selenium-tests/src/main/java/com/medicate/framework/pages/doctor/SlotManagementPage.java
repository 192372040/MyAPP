package com.medicate.framework.pages.doctor;

import com.medicate.framework.pages.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class SlotManagementPage extends BasePage {

    // Locators
    private final By dateInput = By.xpath("//input[contains(@placeholder, 'Date') or contains(@placeholder, 'yyyy-mm-dd')]");
    private final By timeInput = By.xpath("//input[contains(@placeholder, 'Time') or contains(@placeholder, 'hh:mm')]");
    private final By addSlotButton = By.xpath("//button[contains(., 'Add Slot') or contains(@aria-label, 'Add Slot')]");
    private final By statusAlert = By.xpath("//*[contains(text(), 'added successfully') or contains(text(), 'required') or contains(text(), 'exists')]");
    private final By slotListItems = By.xpath("//*[contains(@class, 'slot-item') or contains(@aria-label, 'slot')]");

    public SlotManagementPage(WebDriver driver) {
        super(driver);
    }

    public void addSlot(String date, String time) {
        sendKeys(dateInput, date);
        sendKeys(timeInput, time);
        click(addSlotButton);
    }

    public boolean isAlertDisplayed() {
        return isElementVisible(statusAlert);
    }

    public String getAlertText() {
        return getText(statusAlert);
    }

    public boolean hasSlotsInList() {
        return isElementVisible(slotListItems);
    }
}
