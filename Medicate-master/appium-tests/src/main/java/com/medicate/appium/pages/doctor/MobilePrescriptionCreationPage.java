package com.medicate.appium.pages.doctor;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import com.medicate.appium.pages.MobileBasePage;
import org.openqa.selenium.WebElement;

public class MobilePrescriptionCreationPage extends MobileBasePage {

    @AndroidFindBy(accessibility = "diagnosis_field")
    @iOSXCUITFindBy(accessibility = "diagnosis_field")
    private WebElement diagnosisField;

    @AndroidFindBy(accessibility = "medicines_field")
    @iOSXCUITFindBy(accessibility = "medicines_field")
    private WebElement medicinesField;

    @AndroidFindBy(accessibility = "instructions_field")
    @iOSXCUITFindBy(accessibility = "instructions_field")
    private WebElement instructionsField;

    @AndroidFindBy(accessibility = "create_presc_btn")
    @iOSXCUITFindBy(accessibility = "create_presc_btn")
    private WebElement createPrescButton;

    @AndroidFindBy(accessibility = "download_pdf_btn")
    @iOSXCUITFindBy(accessibility = "download_pdf_btn")
    private WebElement downloadPdfButton;

    public MobilePrescriptionCreationPage(AppiumDriver driver) {
        super(driver);
    }

    public void createPrescription(String diagnosis, String medicines, String instructions) {
        sendKeys(diagnosisField, diagnosis);
        sendKeys(medicinesField, medicines);
        sendKeys(instructionsField, instructions);
        click(createPrescButton);
    }

    public void downloadPdf() {
        click(downloadPdfButton);
    }
}
