package com.medicate.tests;

import com.medicate.framework.driver.DriverFactory;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Optional;
import org.testng.annotations.Parameters;

public class BaseTest {

    protected WebDriver driver;
    protected String baseUrl = "http://localhost:8080"; // Default base URL matching local testing

    @BeforeMethod
    @Parameters({"browser", "headless", "appUrl"})
    public void setUp(@Optional("chrome") String browser, @Optional("true") String headless, @Optional("http://localhost:8080") String appUrl) {
        boolean isHeadless = Boolean.parseBoolean(headless);
        this.baseUrl = appUrl;
        
        // Setup ThreadLocal driver
        driver = DriverFactory.initDriver(browser, isHeadless);
    }

    @AfterMethod(alwaysRun = true)
    public void tearDown() {
        DriverFactory.quitDriver();
    }
}
