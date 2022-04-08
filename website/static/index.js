function deleteSem(semId) {
  fetch("/delete-sem", {
    method: "POST",
    body: JSON.stringify({ semId: semId }),
  }).then((_res) => {
    window.location.href = "/semester";
  });
}

function updateSem(semId) {
  const updatedSem = window.prompt("Enter Updated Semester");
  if (updatedSem) {
    fetch("/update-sem", {
      method: "POST",
      body: JSON.stringify({ semId: semId, updatedSem: updatedSem }),
    }).then((_res) => {
      window.location.href = "/semester";
    });
  }
}

function showSubjects(semId) {
  window.location.href = "/semester/" + semId;
}

function deleteSub(subId, semId) {
  fetch("/delete-sub", {
    method: "POST",
    body: JSON.stringify({ subId: subId }),
  }).then((_res) => {
    window.location.href = "/semester/" + semId;
  });
}

function updateSub(subId, semId) {
  const updatedSub = window.prompt("Enter Updated Subject");
  if (updatedSub) {
    fetch("/update-sub", {
      method: "POST",
      body: JSON.stringify({ subId: subId, updatedSub: updatedSub }),
    }).then((_res) => {
      window.location.href = "/semester/" + semId;
    });
  }
}
