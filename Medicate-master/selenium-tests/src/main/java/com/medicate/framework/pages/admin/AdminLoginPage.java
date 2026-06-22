package com.medicate.framework.pages.admin;

import com.medicate.framework.pages.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class AdminLoginPage extends BasePage {

    // Locators
    private final By hospitalIdInput = By.xpath("//input[contains(@placeholder, 'Hospital ID') or contains(@aria-label, 'Hospital ID')]");
    private final By passwordInput = By.xpath("//input[@type='password' or contains(@placeholder, 'Password')]");
    private final By loginButton = By.xpath("//button[contains(., 'Login') or contains(@aria-label, 'Login')]");
    private final By errorMessage = By.xpath("//*[contains(text(), 'Invalid') or contains(text(), 'required') or contains(@aria-label, 'Invalid')]");

    public AdminLoginPage(WebDriver driver) {
        super(driver);
    }

    public void navigateToLogin(String baseUrl) {
        navigateTo(baseUrl + "/#/admin/login");
    }

    public void login(String hospitalId, String password) {
        sendKeys(hospitalIdInput, hospitalId);
        sendKeys(passwordInput, password);
        click(loginButton);
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
