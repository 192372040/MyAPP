package com.medicate.framework.utils;

import io.qameta.allure.Attachment;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ScreenshotUtils {

    /**
     * Captures a screenshot and saves it to a file, returning the absolute path.
     */
    public static String captureScreenshot(WebDriver driver, String screenshotName) {
        String dateName = new SimpleDateFormat("yyyyMMddhhmmss").format(new Date());
        TakesScreenshot ts = (TakesScreenshot) driver;
        File source = ts.getScreenshotAs(OutputType.FILE);

        String destinationDir = System.getProperty("user.dir") + "/screenshots/";
        try {
            Files.createDirectories(Paths.get(destinationDir));
        } catch (IOException e) {
            System.err.println("Failed to create screenshot directory: " + e.getMessage());
        }

        String destinationPath = destinationDir + screenshotName + "_" + dateName + ".png";
        File finalDestination = new File(destinationPath);
        try {
            Files.copy(source.toPath(), finalDestination.toPath());
        } catch (IOException e) {
            System.err.println("Failed to save screenshot: " + e.getMessage());
        }
        return destinationPath;
    }

    /**
     * Captures a screenshot as a byte array for direct attachment to Allure reports.
     */
    @Attachment(value = "Page Screenshot", type = "image/png")
    public static byte[] captureScreenshotBytes(WebDriver driver) {
        if (driver == null) {
            return new byte[0];
        }
        return ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
    }
}
