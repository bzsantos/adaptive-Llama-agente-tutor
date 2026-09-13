async function triggerStudentHelp(studentId, currentEditorCode, errorMessage) {
    const learningPayload = {
        studentId: studentId,
        actionType: "STUDENT_HELP_REQUEST",
        timestamp: new Date().toISOString(),
        context: {
            activeCode: currentEditorCode,
            lastCompilerError: errorMessage,
            idleTimeSeconds: 145
        }
    };
    const response = await fetch('https://api.tutor.instituicao.edu/v1/mcp/context', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(learningPayload)
    });
    return await response.json();
}