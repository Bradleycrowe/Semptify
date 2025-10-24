*** Settings ***
Library           RequestsLibrary
Suite Setup       Create Session    semptify    ${BASE_URL}

*** Variables ***
${BASE_URL}       http://127.0.0.1:8081

*** Test Cases ***
Health Endpoint Returns 200
    ${resp}=    GET On Session    semptify    /health
    Should Be Equal As Integers    ${resp.status_code}    200

Readyz Endpoint Returns 200
    ${resp}=    GET On Session    semptify    /readyz
    Should Be Equal As Integers    ${resp.status_code}    200

Index Contains Banner
    ${resp}=    GET On Session    semptify    /
    Should Contain    ${resp.text}    Semptify is live

