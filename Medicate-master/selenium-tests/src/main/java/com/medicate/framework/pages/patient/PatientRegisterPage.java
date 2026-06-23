package com.medicate.framework.pages.patient;

import com.medicate.framework.pages.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class PatientRegisterPage extends BasePage {

    // Locators
    private final By nameInput = By.xpath("//input[contains(@placeholder, 'Name')]");
    private final By emailInput = By.xpath("//input[contains(@placeholder, 'Email') or @type='email']");
    private final By phoneInput = By.xpath("//input[contains(@placeholder, 'Phone')]");
    private final By passwordInput = By.xpath("//input[@type='password' and not(contains(@placeholder, 'OTP'))]");
    private final By sendOtpButton = By.xpath("//button[contains(., 'Send OTP') or contains(@aria-label, 'Send OTP')]");
    private final By otpInput = By.xpath("//input[contains(@placeholder, 'OTP') or contains(@placeholder, 'Verification')]");
    private final By registerButton = By.xpath("//button[contains(., 'Register') and not(contains(., 'OTP'))]");
    private final By infoAlert = By.xpath("//*[contains(text(), 'Verification') or contains(text(), 'sent') or contains(text(), 'Invalid')]");

    public PatientRegisterPage(WebDriver driver) {
        super(driver);
    }

    public void navigateToRegister(String baseUrl) {
        navigateTo(baseUrl + "/#/patient/register");
    }

    public void sendOtp(String email) {
        sendKeys(emailInput, email);
        click(sendOtpButton);
    }

    public void fillRegistrationDetails(String name, String phone, String password, String otp) {
        sendKeys(nameInput, name);
        sendKeys(phoneInput, phone);
        sendKeys(passwordInput, password);
        sendKeys(otpInput, otp);
    }

    public void clickRegister() {
        click(registerButton);
    }

    public boolean isAlertMessageDisplayed() {
        return isElementVisible(infoAlert);
    }

    public String getAlertMessageText() {
        return getText(infoAlert);
    }

    public boolean isRegisterBtnVisible() {
        return isElementVisible(registerButton);
    }
}
