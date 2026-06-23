package com.medicate.appium.driver;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.options.UiAutomator2Options;
import io.appium.java_client.ios.IOSDriver;
import io.appium.java_client.ios.options.XCUITestOptions;
import java.net.MalformedURLException;
import java.net.URL;
import java.time.Duration;

public class AppiumDriverFactory {
    private static ThreadLocal<AppiumDriver> driver = new ThreadLocal<>();

    public static AppiumDriver getDriver() {
        return driver.get();
    }

    public static AppiumDriver initializeDriver(String platform, String deviceName, String platformVersion, String udid, String appPath) throws MalformedURLException {
        AppiumDriver localDriver = null;
        URL appiumServerUrl = new URL("http://127.0.0.1:4723/");

        if ("android".equalsIgnoreCase(platform)) {
            UiAutomator2Options options = new UiAutomator2Options()
                    .setDeviceName(deviceName != null ? deviceName : "Android Emulator")
                    .setPlatformVersion(platformVersion != null ? platformVersion : "13.0")
                    .setAutomationName("UiAutomator2")
                    .setApp(appPath != null ? appPath : "app-release.apk")
                    .setNewCommandTimeout(Duration.ofSeconds(300))
                    .setAutoGrantPermissions(true);
            
            if (udid != null && !udid.isEmpty()) {
                options.setUdid(udid);
            }
            localDriver = new AndroidDriver(appiumServerUrl, options);
        } else if ("ios".equalsIgnoreCase(platform)) {
            XCUITestOptions options = new XCUITestOptions()
                    .setDeviceName(deviceName != null ? deviceName : "iPhone 15")
                    .setPlatformVersion(platformVersion != null ? platformVersion : "17.0")
                    .setAutomationName("XCUITest")
                    .setApp(appPath != null ? appPath : "app-release.app")
                    .setWdaLaunchTimeout(Duration.ofSeconds(30))
                    .setNewCommandTimeout(Duration.ofSeconds(300))
                    .setAutoAcceptAlerts(true);
            
            if (udid != null && !udid.isEmpty()) {
                options.setUdid(udid);
            }
            localDriver = new IOSDriver(appiumServerUrl, options);
        } else {
            throw new IllegalArgumentException("Unsupported mobile platform: " + platform);
        }

        localDriver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        driver.set(localDriver);
        return localDriver;
    }

    public static void quitDriver() {
        if (driver.get() != null) {
            driver.get().quit();
            driver.remove();
        }
    }
}
