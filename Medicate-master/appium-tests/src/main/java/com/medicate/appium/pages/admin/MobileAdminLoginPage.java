package com.medicate.appium.pages.admin;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSXCUITFindBy;
import com.medicate.appium.pages.MobileBasePage;
import org.openqa.selenium.WebElement;

public class MobileAdminLoginPage extends MobileBasePage {

    @AndroidFindBy(accessibility = "hospital_id_field")
    @iOSXCUITFindBy(accessibility = "hospital_id_field")
    private WebElement hospitalIdField;

    @AndroidFindBy(accessibility = "password_field")
    @iOSXCUITFindBy(accessibility = "password_field")
    private WebElement passwordField;

    @AndroidFindBy(accessibility = "login_btn")
    @iOSXCUITFindBy(accessibility = "login_btn")
    private WebElement loginButton;

    @AndroidFindBy(accessibility = "toast_message")
    @iOSXCUITFindBy(accessibility = "toast_message")
    private WebElement toastMessage;

    public MobileAdminLoginPage(AppiumDriver driver) {
        super(driver);
    }

    public void login(String hospitalId, String password) {
        sendKeys(hospitalIdField, hospitalId);
        sendKeys(passwordField, password);
        click(loginButton);
    }

    public String getToastMessage() {
        return getText(toastMessage);
    }
}
