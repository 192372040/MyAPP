package com.medicate.appium.pages.doctor;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import com.medicate.appium.pages.MobileBasePage;
import org.openqa.selenium.WebElement;

public class MobileDoctorLoginPage extends MobileBasePage {

    @AndroidFindBy(accessibility = "doc_id_field")
    @iOSXCUITFindBy(accessibility = "doc_id_field")
    private WebElement doctorIdField;

    @AndroidFindBy(accessibility = "doc_pass_field")
    @iOSXCUITFindBy(accessibility = "doc_pass_field")
    private WebElement passwordField;

    @AndroidFindBy(accessibility = "doc_login_btn")
    @iOSXCUITFindBy(accessibility = "doc_login_btn")
    private WebElement loginButton;

    public MobileDoctorLoginPage(AppiumDriver driver) {
        super(driver);
    }

    public void login(String doctorId, String password) {
        sendKeys(doctorIdField, doctorId);
        sendKeys(passwordField, password);
        click(loginButton);
    }
}
