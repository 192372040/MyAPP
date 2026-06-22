package com.medicate.framework.pages.doctor;

import com.medicate.framework.pages.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class PrescriptionCreationPage extends BasePage {

    // Locators
    private final By activeAppointmentItem = By.xpath("//*[contains(@class, 'appointment-item') or contains(@aria-label, 'Appointment')]");
    private final By diagnosisInput = By.xpath("//input[contains(@placeholder, 'Diagnosis') or contains(@aria-label, 'Diagnosis')]");
    private final By medicinesInput = By.xpath("//input[contains(@placeholder, 'Medicines') or contains(@aria-label, 'Medicines')]");
    private final By instructionsInput = By.xpath("//input[contains(@placeholder, 'Instructions') or contains(@aria-label, 'Instructions')]");
    private final By followUpInput = By.xpath("//input[contains(@placeholder, 'Follow') or contains(@aria-label, 'Follow')]");
    private final By submitButton = By.xpath("//button[contains(., 'Save') or contains(., 'Create') or contains(@aria-label, 'Save')]");
    private final By statusAlert = By.xpath("//*[contains(text(), 'saved') or contains(text(), 'completed') or contains(text(), 'required')]");
    private final By downloadPdfButton = By.xpath("//button[contains(., 'Download') or contains(@aria-label, 'Download')]");

    public PrescriptionCreationPage(WebDriver driver) {
        super(driver);
    }

    public void selectAppointment() {
        click(activeAppointmentItem);
    }

    public void fillPrescriptionDetails(String diagnosis, String medicines, String instructions, String followUp) {
        sendKeys(diagnosisInput, diagnosis);
        sendKeys(medicinesInput, medicines);
        sendKeys(instructionsInput, instructions);
        sendKeys(followUpInput, followUp);
    }

    public void clickSubmit() {
        click(submitButton);
    }

    public boolean isAlertDisplayed() {
        return isElementVisible(statusAlert);
    }

    public String getAlertText() {
        return getText(statusAlert);
    }

    public boolean isDownloadPdfBtnVisible() {
        return isElementVisible(downloadPdfButton);
    }

    public void downloadPdf() {
        click(downloadPdfButton);
    }
}
