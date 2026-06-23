package com.medicate.framework.pages.doctor;

import com.medicate.framework.pages.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class DoctorRegisterPage extends BasePage {

    // Locators
    private final By nameInput = By.xpath("//input[contains(@placeholder, 'Name') or contains(@aria-label, 'Name')]");
    private final By specializationInput = By.xpath("//input[contains(@placeholder, 'Specialization') or contains(@aria-label, 'Specialization')]");
    private final By qualificationInput = By.xpath("//input[contains(@placeholder, 'Qualification') or contains(@aria-label, 'Qualification')]");
    private final By experienceInput = By.xpath("//input[contains(@placeholder, 'Experience') or contains(@aria-label, 'Experience')]");
    private final By phoneInput = By.xpath("//input[contains(@placeholder, 'Phone') or contains(@aria-label, 'Phone')]");
    private final By emailInput = By.xpath("//input[contains(@placeholder, 'Email') or @type='email']");
    private final By passwordInput = By.xpath("//input[@type='password']");
    private final By registerButton = By.xpath("//button[contains(., 'Register') or contains(@aria-label, 'Register')]");
    private final By backButton = By.xpath("//button[contains(., 'Back') or contains(@aria-label, 'Back')]");
    private final By errorMessage = By.xpath("//*[contains(text(), 'required') or contains(text(), 'already') or contains(text(), 'Invalid')]");

    public DoctorRegisterPage(WebDriver driver) {
        super(driver);
    }

    public void navigateToRegister(String baseUrl) {
        navigateTo(baseUrl + "/#/doctor/register");
    }

    public void register(String name, String spec, String qual, String exp, String phone, String email, String password) {
        sendKeys(nameInput, name);
        sendKeys(specializationInput, spec);
        sendKeys(qualificationInput, qual);
        sendKeys(experienceInput, exp);
        sendKeys(phoneInput, phone);
        sendKeys(emailInput, email);
        sendKeys(passwordInput, password);
        click(registerButton);
    }

    public void clickBack() {
        click(backButton);
    }

    public boolean isErrorMessageDisplayed() {
        return isElementVisible(errorMessage);
    }

    public String getErrorMessageText() {
        return getText(errorMessage);
    }

    public boolean isRegisterBtnVisible() {
        return isElementVisible(registerButton);
    }
}
