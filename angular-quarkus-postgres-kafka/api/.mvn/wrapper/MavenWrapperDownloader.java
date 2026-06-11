/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

import java.io.IOException;
import java.io.InputStream;
import java.net.Authenticator;
import java.net.PasswordAuthentication;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

public class MavenWrapperDownloader {

    private static final String DEFAULT_WRAPPER_URL =
            "https://repo.maven.apache.org/maven2/org/apache/maven/wrapper/maven-wrapper/3.2.0/maven-wrapper-3.2.0.jar";

    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: MavenWrapperDownloader <wrapperUrl> <wrapperJarPath>");
            System.exit(1);
        }

        String wrapperUrl = args[0];
        String wrapperJarPath = args[1];

        System.out.println(" - Downloading Maven wrapper from: " + wrapperUrl);

        Path outputFile = Paths.get(wrapperJarPath);
        if (!Files.isDirectory(outputFile.getParent())) {
            System.err.println(" - Output directory does not exist: " + outputFile.getParent());
            System.exit(1);
        }

        try {
            String userHome = System.getProperty("user.home");
            String mavenUserSettingsXml = userHome + "/.m2/settings.xml";
            if (Files.exists(Paths.get(mavenUserSettingsXml))) {
                System.out.println(" - Found Maven settings.xml at: " + mavenUserSettingsXml);
            }

            URL url = new URL(wrapperUrl);
            String username = System.getProperty("maven.wrapper.username");
            String password = System.getProperty("maven.wrapper.password");
            if (username != null && password != null) {
                Authenticator.setDefault(new Authenticator() {
                    @Override
                    protected PasswordAuthentication getPasswordAuthentication() {
                        return new PasswordAuthentication(username, password.toCharArray());
                    }
                });
            }

            System.out.println(" - Downloading to: " + outputFile);
            try (InputStream in = url.openStream()) {
                Files.copy(in, outputFile, StandardCopyOption.REPLACE_EXISTING);
            }
            System.out.println(" - Download complete.");
        } catch (IOException e) {
            System.err.println(" - Error downloading Maven wrapper: " + e.getMessage());
            if (DEFAULT_WRAPPER_URL.equals(wrapperUrl)) {
                System.err.println(" - The default wrapper URL may be unavailable.");
                System.err.println(" - Try setting MVNW_REPOURL to a mirror.");
            }
            System.exit(1);
        }
    }
}
