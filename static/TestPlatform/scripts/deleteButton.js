$(".if-del-btn").on("click", function () {
    var delE = $(this);
    var if_id = delE.attr("if_value");
    console.log(if_id);
    swal({
        title: "",
        text: "确定删除吗？",
        type: "warning",
        showCancelButton: "true",
        showConfirmButton: "true",
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        animation: "slide-from-top"
    }, function () {
        $.ajax({
            type: "post",
            url: "/platform/interface_delete/",
            traditional: true,
            dataType: "json",
            data: {"if_id": if_id},
        }).done(function (data) {
            if (data.status === "0") {
                swal("操作成功!", "已成功删除数据！", "success");
                delE.parent().parent().remove();
            } else {
                swal("OMG", "删除操作失败了!", "error");
            }
        }).error(function (data) {
            swal("OMG", "删除操作失败了!", "error");
        });
    });
});


