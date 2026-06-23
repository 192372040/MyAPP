package com.medicate.appium.pages.patient;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import com.medicate.appium.pages.MobileBasePage;
import org.openqa.selenium.WebElement;

public class MobilePatientLoginPage extends MobileBasePage {

    @AndroidFindBy(accessibility = "pat_email_field")
    @iOSXCUITFindBy(accessibility = "pat_email_field")
    private WebElement emailField;

    @AndroidFindBy(accessibility = "pat_pass_field")
    @iOSXCUITFindBy(accessibility = "pat_pass_field")
    private WebElement passwordField;

    @AndroidFindBy(accessibility = "pat_login_btn")
    @iOSXCUITFindBy(accessibility = "pat_login_btn")
    private WebElement loginButton;

    public MobilePatientLoginPage(AppiumDriver driver) {
        super(driver);
    }

    public void login(String email, String password) {
        sendKeys(emailField, email);
        sendKeys(passwordField, password);
        click(loginButton);
    }
}
