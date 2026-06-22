package com.medicate.framework.pages.doctor;

import com.medicate.framework.pages.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class DoctorLoginPage extends BasePage {

    // Locators
    private final By doctorIdInput = By.xpath("//input[contains(@placeholder, 'Doctor ID') or contains(@aria-label, 'Doctor ID')]");
    private final By passwordInput = By.xpath("//input[@type='password']");
    private final By loginButton = By.xpath("//button[contains(., 'Login') or contains(@aria-label, 'Login')]");
    private final By errorMessage = By.xpath("//*[contains(text(), 'required') or contains(text(), 'Invalid') or contains(@aria-label, 'Error')]");
    private final By welcomeHeader = By.xpath("//*[contains(text(), 'Welcome, Dr.')]");

    public DoctorLoginPage(WebDriver driver) {
        super(driver);
    }

    public void navigateToLogin(String baseUrl) {
        navigateTo(baseUrl + "/#/doctor/login");
    }

    public void login(String doctorId, String password) {
        sendKeys(doctorIdInput, doctorId);
        sendKeys(passwordInput, password);
        click(loginButton);
    }

    public boolean isWelcomeHeaderDisplayed() {
        return isElementVisible(welcomeHeader);
    }

    public String getWelcomeHeaderText() {
        return getText(welcomeHeader);
    }

    public boolean isErrorMessageDisplayed() {
        return isElementVisible(errorMessage);
    }

    public String getErrorMessageText() {
        return getText(errorMessage);
    }

    public boolean isLoginBtnVisible() {
        return isElementVisible(loginButton);
    }
}
