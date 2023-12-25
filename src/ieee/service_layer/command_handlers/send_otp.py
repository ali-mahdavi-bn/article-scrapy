from account.domain import commands
from account.domain.services.otp import OtpService, OtpError
from backbone.exception import BadRequestException
from unit_of_work import UnitOfWork


def send_otp(command: commands.SendOtpCommand, uow: UnitOfWork):
    with uow:
        otp_service = OtpService(uow)
        try:
            otp, time_left = otp_service.create(command.mobile)
            uow.commit()
            if otp_service.is_created_new_otp:
                otp_service.send(otp)
                return {"time_left": time_left, "message": "otp generated successfully"}

            return {"time_left": time_left, "message": f"regenerate otp until {time_left} second",
                    "is_created_new_otp": otp_service.is_created_new_otp}
        except OtpError as e:
            raise BadRequestException(e.__str__())
