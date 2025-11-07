import base64

from .login import (QRLoginType, QR, get_qrcode, check_qrcode, QRCodeLoginEvents)


async def get_refresh():
    from .utils.session import get_session
    credential = get_session().credential
    print(f"credential的值: {credential}")
    refresh_bool = await credential.refresh()

    return {
        "refresh": refresh_bool, "credential": credential
    }


async def get_qrdata(login_type: QRLoginType = QRLoginType.QQ):
    """
    获取登录二维码
    Args:
        login_type: 登录类型

    Returns:

    """

    qr = await get_qrcode(login_type)
    image_str = base64.b64encode(qr.data).decode('utf-8')
    image_data = f"data:image/png;base64,{image_str}"
    return {"image_base64": image_data, "qr_type": qr.qr_type,
            "mimetype": qr.mimetype, "identifier": qr.identifier}


async def check_qrdata(qr_type: QRLoginType, mimetype: str, identifier: str):
    qr_data = QR(data=None,
                 qr_type=qr_type,
                 mimetype=mimetype,
                 identifier=identifier)

    print(f"QR的值: {qr_data}")

    event, credential = await check_qrcode(qr_data)
    print(f"当前状态: {event.name}")

    if event == QRCodeLoginEvents.DONE:
        print(f"登录成功! MusicID: {credential.musicid}")
    if event == QRCodeLoginEvents.TIMEOUT:
        print("二维码已过期,请重新获取")

    return {"event": event.name, "credential": credential}
