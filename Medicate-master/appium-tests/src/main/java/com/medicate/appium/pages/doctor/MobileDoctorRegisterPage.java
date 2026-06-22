package com.medicate.appium.pages.doctor;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import com.medicate.appium.pages.MobileBasePage;
import org.openqa.selenium.WebElement;

public class MobileDoctorRegisterPage extends MobileBasePage {

    @AndroidFindBy(accessibility = "doc_name_field")
    @iOSXCUITFindBy(accessibility = "doc_name_field")
    private WebElement nameField;

    @AndroidFindBy(accessibility = "doc_spec_field")
    @iOSXCUITFindBy(accessibility = "doc_spec_field")
    private WebElement specializationField;

    @AndroidFindBy(accessibility = "doc_qual_field")
    @iOSXCUITFindBy(accessibility = "doc_qual_field")
    private WebElement qualificationField;

    @AndroidFindBy(accessibility = "doc_exp_field")
    @iOSXCUITFindBy(accessibility = "doc_exp_field")
    private WebElement experienceField;

    @AndroidFindBy(accessibility = "doc_phone_field")
    @iOSXCUITFindBy(accessibility = "doc_phone_field")
    private WebElement phoneField;

    @AndroidFindBy(accessibility = "doc_email_field")
    @iOSXCUITFindBy(accessibility = "doc_email_field")
    private WebElement emailField;

    @AndroidFindBy(accessibility = "doc_pass_field")
    @iOSXCUITFindBy(accessibility = "doc_pass_field")
    private WebElement passwordField;

    @AndroidFindBy(accessibility = "doc_register_btn")
    @iOSXCUITFindBy(accessibility = "doc_register_btn")
    private WebElement registerButton;

    public MobileDoctorRegisterPage(AppiumDriver driver) {
        super(driver);
    }

    public void register(String name, String spec, String qual, String exp, String phone, String email, String password) {
        sendKeys(nameField, name);
        sendKeys(specializationField, spec);
        sendKeys(qualificationField, qual);
        sendKeys(experienceField, exp);
        sendKeys(phoneField, phone);
        sendKeys(emailField, email);
        sendKeys(passwordField, password);
        click(registerButton);
    }
}
