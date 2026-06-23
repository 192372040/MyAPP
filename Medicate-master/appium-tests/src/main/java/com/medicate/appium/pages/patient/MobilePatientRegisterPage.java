package com.medicate.appium.pages.patient;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import com.medicate.appium.pages.MobileBasePage;
import org.openqa.selenium.WebElement;

public class MobilePatientRegisterPage extends MobileBasePage {

    @AndroidFindBy(accessibility = "pat_name_field")
    @iOSXCUITFindBy(accessibility = "pat_name_field")
    private WebElement nameField;

    @AndroidFindBy(accessibility = "pat_email_field")
    @iOSXCUITFindBy(accessibility = "pat_email_field")
    private WebElement emailField;

    @AndroidFindBy(accessibility = "pat_phone_field")
    @iOSXCUITFindBy(accessibility = "pat_phone_field")
    private WebElement phoneField;

    @AndroidFindBy(accessibility = "pat_pass_field")
    @iOSXCUITFindBy(accessibility = "pat_pass_field")
    private WebElement passwordField;

    @AndroidFindBy(accessibility = "pat_send_otp_btn")
    @iOSXCUITFindBy(accessibility = "pat_send_otp_btn")
    private WebElement sendOtpButton;

    @AndroidFindBy(accessibility = "pat_otp_field")
    @iOSXCUITFindBy(accessibility = "pat_otp_field")
    private WebElement otpField;

    @AndroidFindBy(accessibility = "pat_register_btn")
    @iOSXCUITFindBy(accessibility = "pat_register_btn")
    private WebElement registerButton;

    public MobilePatientRegisterPage(AppiumDriver driver) {
        super(driver);
    }

    public void register(String name, String email, String phone, String password, String otp) {
        sendKeys(nameField, name);
        sendKeys(emailField, email);
        sendKeys(phoneField, phone);
        sendKeys(passwordField, password);
        click(sendOtpButton);
        sendKeys(otpField, otp);
        click(registerButton);
    }
}
