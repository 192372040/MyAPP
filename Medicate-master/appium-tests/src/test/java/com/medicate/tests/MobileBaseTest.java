package com.medicate.tests;

import io.appium.java_client.AppiumDriver;
import com.medicate.appium.driver.AppiumDriverFactory;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Optional;
import org.testng.annotations.Parameters;
import java.net.MalformedURLException;

public class MobileBaseTest {
    protected AppiumDriver driver;

    @BeforeClass
    @Parameters({"platform", "deviceName", "platformVersion", "udid", "appPath"})
    public void setUp(
            @Optional("android") String platform,
            @Optional("Android Emulator") String deviceName,
            @Optional("13.0") String platformVersion,
            @Optional("") String udid,
            @Optional("app-release.apk") String appPath) {
        try {
            driver = AppiumDriverFactory.initializeDriver(platform, deviceName, platformVersion, udid, appPath);
        } catch (MalformedURLException e) {
            e.printStackTrace();
            throw new RuntimeException("Appium Server URL is malformed or invalid: " + e.getMessage());
        }
    }

    @AfterClass
    public void tearDown() {
        AppiumDriverFactory.quitDriver();
    }
}
