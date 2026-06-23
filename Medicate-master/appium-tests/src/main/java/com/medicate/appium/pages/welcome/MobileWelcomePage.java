package com.medicate.appium.pages.welcome;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import com.medicate.appium.pages.MobileBasePage;
import org.openqa.selenium.WebElement;

public class MobileWelcomePage extends MobileBasePage {

    @AndroidFindBy(accessibility = "admin_portal_btn")
    @iOSXCUITFindBy(accessibility = "admin_portal_btn")
    private WebElement adminPortalButton;

    @AndroidFindBy(accessibility = "doctor_portal_btn")
    @iOSXCUITFindBy(accessibility = "doctor_portal_btn")
    private WebElement doctorPortalButton;

    @AndroidFindBy(accessibility = "patient_portal_btn")
    @iOSXCUITFindBy(accessibility = "patient_portal_btn")
    private WebElement patientPortalButton;

    public MobileWelcomePage(AppiumDriver driver) {
        super(driver);
    }

    public void clickAdminPortal() {
        click(adminPortalButton);
    }

    public void clickDoctorPortal() {
        click(doctorPortalButton);
    }

    public void clickPatientPortal() {
        click(patientPortalButton);
    }
}
