package com.medicate.framework.pages.patient;

import com.medicate.framework.pages.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class AppointmentBookingPage extends BasePage {

    // Locators
    private final By hospitalDropdown = By.xpath("//*[contains(@class, 'hospital-dropdown') or contains(@aria-label, 'Select Hospital')]");
    private final By doctorDropdown = By.xpath("//*[contains(@class, 'doctor-dropdown') or contains(@aria-label, 'Select Doctor')]");
    private final By slotOption = By.xpath("//*[contains(@class, 'slot-option') or contains(@aria-label, '10:30') or contains(@aria-label, 'Slot')]");
    private final By symptomsInput = By.xpath("//input[contains(@placeholder, 'symptoms') or contains(@placeholder, 'Symptoms') or @type='text']");
    private final By bookButton = By.xpath("//button[contains(., 'Book') or contains(@aria-label, 'Book')]");
    private final By successMessage = By.xpath("//*[contains(text(), 'booked successfully') or contains(@aria-label, 'Success')]");

    public AppointmentBookingPage(WebDriver driver) {
        super(driver);
    }

    public void selectHospitalAndDoctor(String hospitalName, String doctorName) {
        click(hospitalDropdown);
        click(By.xpath("//*[contains(text(), '" + hospitalName + "') or contains(@aria-label, '" + hospitalName + "')]"));
        
        click(doctorDropdown);
        click(By.xpath("//*[contains(text(), '" + doctorName + "') or contains(@aria-label, '" + doctorName + "')]"));
    }

    public void selectSlot() {
        click(slotOption);
    }

    public void enterSymptoms(String symptoms) {
        sendKeys(symptomsInput, symptoms);
    }

    public void clickBook() {
        click(bookButton);
    }

    public boolean isBookingSuccessful() {
        return isElementVisible(successMessage);
    }

    public String getSuccessMessageText() {
        return getText(successMessage);
    }
}
